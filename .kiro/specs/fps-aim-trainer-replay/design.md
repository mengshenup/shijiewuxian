# FPS Aim Trainer - Replay System Design Document

## Overview

本文档描述录像回放系统的设计，这是FPS瞄准训练系统的可选扩展功能。录像回放系统允许玩家记录训练会话，并在相邻房间回放历史录像作为对手，创造竞争氛围。

**核心特性：**
- **录像记录**：自动记录每次训练会话（约240 bytes/会话）
- **超压缩编码**：使用智能事件编码，极致优化数据大小
- **ELO匹配**：根据玩家ELO从本地历史录像中选择相近水平的对手
- **回放系统**：在相邻房间回放录像，完整的角色动画和射击效果
- **本地存储**：所有录像保存在本地，无需服务器

**系统架构：**
玩家在中间房间训练，左右相邻房间通过透明隔板可见。系统从玩家的历史录像中选择2个ELO相近的回放作为对手，创造与过去的自己对战的体验。

## Core Components

### 1. UReplayRecorder

录像记录组件，使用智能事件编码。

**职责：**
- 记录训练会话的关键事件
- 使用超压缩编码（约240 bytes/会话）
- 保存录像到本地磁盘

**关键接口：**
```cpp
class UReplayRecorder : public UActorComponent
{
public:
    void StartRecording();
    void StopRecording();
    void SaveReplay();
    
    // 记录事件
    void RecordTargetAcquired(uint8 TargetID);
    void RecordShot(uint8 TargetID);
    void RecordHit(uint8 TargetID);
    void RecordMiss(uint8 TargetID);
    
private:
    FUltraCompactReplay CurrentReplay;
    float LastEventTime;
    bool bIsRecording;
};
```

### 2. UReplayMatcher

ELO匹配系统，从本地历史录像中选择对手。

**职责：**
- 扫描本地保存的录像文件
- 根据ELO范围筛选录像
- 选择2个最接近的历史录像作为对手

**关键接口：**
```cpp
class UReplayMatcher : public UObject
{
public:
    // 匹配录像
    TArray<FReplayData*> FindOpponents(float CurrentELO, int32 Count = 2);
    
    // 录像库管理
    void ScanLocalReplays();
    TArray<FReplayMetadata> GetAvailableReplays() const;
    
private:
    TArray<FReplayMetadata> LocalReplayCache;
    float ELOMatchRange;  // ±200 ELO
};
```

### 3. AReplayOpponent

回放对手角色，播放历史录像。

**职责：**
- 加载并播放录像数据
- 根据事件流执行动作（瞄准、射击）
- 提供完整的视觉反馈

**关键接口：**
```cpp
class AReplayOpponent : public ACharacter
{
public:
    void LoadReplay(const FUltraCompactReplay& ReplayData);
    void StartPlayback();
    void StopPlayback();
    
protected:
    virtual void Tick(float DeltaTime) override;
    
private:
    FUltraCompactReplay LoadedReplay;
    int32 CurrentEventIndex;
    float PlaybackTime;
    bool bIsPlaying;
    
    // 回放逻辑
    void ProcessNextEvent();
    void ExecuteEvent(const FCompactReplayEvent& Event);
    void AimAtTarget(uint8 TargetID);
    void SimulateShot();
};
```

## Data Models

### FCompactReplayEvent

超压缩事件结构（3 bytes）。

```cpp
struct FCompactReplayEvent
{
    uint8 EventType : 2;      // 事件类型：0=瞄准, 1=射击, 2=命中, 3=未命中
    uint8 TargetID : 6;       // 目标ID (0-63)
    uint16 TimeDeltaMs : 16;  // 距上次事件的时间（毫秒）
    
    // 总计：24 bits = 3 bytes
};
```

### FUltraCompactReplay

超压缩录像数据结构（约240 bytes）。

```cpp
struct FUltraCompactReplay
{
    // 头部（20 bytes）
    uint32 Version;              // 版本号
    uint32 PlayerELO;            // 玩家ELO
    uint16 TotalShots;           // 总射击次数
    uint16 TotalHits;            // 总命中次数
    uint16 SessionDurationMs;    // 会话时长（毫秒）
    uint8 TargetSequenceSeed;    // 目标生成随机种子
    uint8 Reserved[5];           // 保留字段
    
    // 事件流（约220 bytes）
    TArray<FCompactReplayEvent> Events;  // 约80个事件
};
```

### FReplayMetadata

录像元数据（用于匹配和显示）。

```cpp
struct FReplayMetadata
{
    FString ReplayID;           // 唯一ID
    FDateTime RecordedDate;     // 录制日期
    float PlayerELO;            // 玩家ELO
    float HitRate;              // 命中率
    int32 TotalShots;           // 总射击次数
    int32 TotalHits;            // 总命中次数
    FString FilePath;           // 文件路径
};
```

## Replay System Design

### Recording Process

**录制流程：**
```
训练开始
  ↓
初始化UReplayRecorder
  ↓
记录初始状态（ELO、随机种子）
  ↓
训练进行中：
  - 玩家瞄准目标 → 记录TargetAcquired事件
  - 玩家射击 → 记录Shot事件
  - 命中/未命中 → 记录Hit/Miss事件
  ↓
训练结束
  ↓
保存FUltraCompactReplay到本地
  ↓
文件命名：Replay_{Timestamp}_{ELO}.sav
```

**事件记录策略：**
- 只记录有意义的事件（瞄准、射击、命中）
- 不记录每帧的位置和旋转
- 使用时间差编码（相对时间，节省空间）
- 使用位域压缩（3 bytes/事件）

### Playback Process

**回放流程：**
```
训练开始前
  ↓
UReplayMatcher扫描本地录像
  ↓
根据当前ELO筛选录像（±200范围）
  ↓
选择2个最接近的录像
  ↓
生成2个AReplayOpponent到相邻房间
  ↓
加载录像数据到回放对手
  ↓
训练开始，同步启动回放
  ↓
回放对手按事件流执行动作：
  - TargetAcquired → 转向目标
  - Shot → 播放射击动画和音效
  - Hit → 销毁目标，生成新目标
  ↓
训练结束，停止回放
```

### Local Storage

**存储位置：**
```
Windows: {ProjectDir}/Saved/SaveGames/Replays/
文件格式：Replay_{Timestamp}_{ELO}.sav
```

**UE5 SaveGame实现：**
```cpp
class UReplaySaveGame : public USaveGame
{
    GENERATED_BODY()
    
public:
    UPROPERTY()
    FUltraCompactReplay ReplayData;
    
    UPROPERTY()
    FReplayMetadata Metadata;
};
```

## ELO Matching System

**匹配算法：**
```cpp
TArray<FReplayData*> UReplayMatcher::FindOpponents(float CurrentELO, int32 Count)
{
    // 1. 扫描本地录像
    ScanLocalReplays();
    
    // 2. 筛选ELO范围内的录像
    float MinELO = CurrentELO - 200;
    float MaxELO = CurrentELO + 200;
    
    TArray<FReplayMetadata> Candidates;
    for (const FReplayMetadata& Replay : LocalReplayCache)
    {
        if (Replay.PlayerELO >= MinELO && Replay.PlayerELO <= MaxELO)
        {
            Candidates.Add(Replay);
        }
    }
    
    // 3. 按ELO距离排序
    Candidates.Sort([CurrentELO](const FReplayMetadata& A, const FReplayMetadata& B)
    {
        float DistA = FMath::Abs(A.PlayerELO - CurrentELO);
        float DistB = FMath::Abs(B.PlayerELO - CurrentELO);
        return DistA < DistB;
    });
    
    // 4. 选择最接近的N个
    TArray<FReplayData*> Selected;
    for (int32 i = 0; i < FMath::Min(Count, Candidates.Num()); i++)
    {
        FReplayData* Replay = LoadReplay(Candidates[i].FilePath);
        Selected.Add(Replay);
    }
    
    return Selected;
}
```

## Room Layout with Replay Opponents

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  左侧房间     │  │  玩家房间     │  │  右侧房间     │
│              │  │              │  │              │
│  回放对手1    │  │    玩家      │  │  回放对手2    │
│  (过去的自己) │  │  (当前训练)  │  │  (过去的自己) │
│              │  │              │  │              │
│  白板 + 目标  │  │  白板 + 目标  │  │  白板 + 目标  │
└──────────────┘  └──────────────┘  └──────────────┘
      ↑                  ↑                  ↑
   透明隔板           透明隔板           透明隔板
   (可见不可射)       (可见不可射)
```

## Implementation Notes

**此功能为可选扩展，建议在核心功能完成后再实现。**

**实现优先级：**
1. 先实现核心训练系统（目标、统计、历史数据）
2. 再实现录像记录功能
3. 最后实现回放和相邻房间系统

**数据量分析：**
- 单个录像：约240 bytes
- 100个录像：约24 KB
- 1000个录像：约240 KB
- 存储成本极低，适合本地保存

