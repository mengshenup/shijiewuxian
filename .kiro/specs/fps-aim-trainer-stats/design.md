# FPS Aim Trainer - Statistics System Design Document

## Overview

本文档描述统计数据系统的设计，这是FPS瞄准训练系统的扩展功能。统计系统负责追踪玩家表现、保存历史数据、显示曲线图和3D UI界面。

**核心特性：**
- **统计追踪**：追踪射击次数、命中次数、命中率
- **历史数据**：永久保存所有训练记录
- **曲线图**：显示历史数据趋势（最近30场）
- **3D UI**：VR风格的3D统计界面
- **分页浏览**：支持查看任意时间段的历史数据

## Core Components

### 1. UStatisticsTracker

统计数据追踪组件。

```cpp
class UStatisticsTracker : public UActorComponent
{
public:
    void IncrementShotCount();
    void IncrementHitCount();
    void ResetStatistics();
    
    int32 GetTotalShots() const { return TotalShots; }
    int32 GetTotalHits() const { return TotalHits; }
    float GetHitRate() const;
    
private:
    int32 TotalShots;
    int32 TotalHits;
};
```

### 2. UHistoryTracker

历史数据追踪和持久化组件。

```cpp
class UHistoryTracker : public UActorComponent
{
public:
    void SaveSessionData(const FTrainingStatistics& Stats);
    TArray<FSessionRecord> GetRecentSessions(int32 Count = 30) const;
    TArray<FSessionRecord> GetSessionsInRange(int32 StartIndex, int32 Count) const;
    
    void LoadHistoryFromDisk();
    void SaveHistoryToDisk();
    
private:
    TArray<FSessionRecord> SessionHistory;
};
```

### 3. AStatisticsWidget3D

3D统计界面Actor（VR风格）。

```cpp
class AStatisticsWidget3D : public AActor
{
public:
    void UpdateStatistics(const FTrainingStatistics& Stats);
    void UpdateChart(const TArray<FSessionRecord>& History);
    
    void NextPage();
    void PreviousPage();
    
    void Show();
    void Hide();
    
private:
    UPROPERTY(VisibleAnywhere)
    UWidgetComponent* WidgetComponent;
    
    UPROPERTY(VisibleAnywhere)
    UStaticMeshComponent* PanelMesh;
};
```

### 4. UChartWidget

历史数据曲线图Widget组件。

```cpp
class UChartWidget : public UUserWidget
{
public:
    void UpdateChartData(const TArray<FSessionRecord>& Data);
    void SetChartType(EChartType Type);
    
protected:
    virtual int32 NativePaint(...) const override;
    
private:
    void DrawAxes(...) const;
    void DrawDataLine(...) const;
    void DrawLabels(...) const;
};
```

## Data Models

### FTrainingStatistics
```cpp
struct FTrainingStatistics
{
    int32 TotalShots;
    int32 TotalHits;
    float HitRate;
    float SessionDuration;
};
```

### FSessionRecord
```cpp
struct FSessionRecord
{
    FDateTime Timestamp;
    int32 SessionNumber;
    int32 TotalShots;
    int32 TotalHits;
    float HitRate;
};
```

## Implementation Notes

**此功能为扩展功能，建议在基础房间和目标系统完成后再实现。**

详细设计请参考之前的完整文档。

