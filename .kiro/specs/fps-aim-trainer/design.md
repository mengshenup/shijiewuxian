# FPS Aim Trainer - Core Room Setup Design Document

## Overview

本设计文档描述FPS瞄准训练系统的核心房间搭建功能。使用纯C++代码实现，无需任何编辑器操作。

**引擎版本要求：**
- **Unreal Engine 5.7.0**（源码版本）
- C++ 标准：C++20
- 编译器：MSVC 2022（Windows）
- 项目名称：shijiewuxian

**核心目标：**
- 通过C++代码创建3个训练房间（中间玩家房间 + 左右对手房间）
- 使用透明隔板分隔房间，可以看到相邻房间
- 在中间房间生成玩家（第一人称角色）
- 左右对手房间暂时空置
- **完全通过代码实现，AI无需打开编辑器**

**实现方式：**
- 在Actor构造函数中使用`CreateDefaultSubobject`创建所有组件
- 使用`ConstructorHelpers::FObjectFinder`加载引擎自带资源
- 在GameMode的`BeginPlay`中使用`SpawnActor`生成房间
- 人类可以在AI完成后选择性地在编辑器中调整参数


## Room Layout

### 3D空间布局（无缝连接）

```
俯视图：

┌──────────────┬──────────────┬──────────────┐
│              │              │              │
│  左侧房间     │  玩家房间     │  右侧房间     │
│  (对手房间1)  │  (中间)      │  (对手房间2)  │
│              │              │              │
│              │              │              │
│              │    玩家      │              │
│              │              │              │
│              │              │              │
│              │              │              │
└──────────────┴──────────────┴──────────────┘
               ↑              ↑
           透明隔板        透明隔板
           (共享墙)        (共享墙)
```

### 房间尺寸

**整体结构：**
- 总宽度：1800 cm (18米) - 3个房间并排
- 总深度：800 cm (8米)
- 总高度：400 cm (4米)

**单个房间：**
- 宽度（X轴）：600 cm (6米)
- 深度（Y轴）：800 cm (8米)
- 高度（Z轴）：400 cm (4米)

**透明隔板（共享墙）：**
- 位置：X = -300 和 X = +300
- 厚度：10 cm
- 高度：400 cm
- 深度：800 cm

**坐标系统：**
```
X轴：左右方向（左负右正）
Y轴：前后方向（后负前正）
Z轴：上下方向（下负上正）

房间划分：
- 左侧房间：X = -900 到 -300
- 中间房间：X = -300 到 +300
- 右侧房间：X = +300 到 +900

透明墙位置：
- 左侧透明墙：X = -300
- 右侧透明墙：X = +300

玩家出生点：
- 位置：X = 0, Y = 0, Z = 100
```


## Core Components

### 1. ATrainingRoom

训练房间Actor，包含完整的房间结构（地板、天花板、墙壁、透明隔板）。

**UE5.7.0实现：**

```cpp
// TrainingRoom.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "TrainingRoom.generated.h"

// Forward declarations
class UStaticMeshComponent;
class UMaterialInterface;

UCLASS()
class SHIJIEWUXIAN_API ATrainingRoom : public AActor
{
    GENERATED_BODY()
    
public:
    ATrainingRoom();
    
    // Room information
    FVector GetRoomCenter() const { return GetActorLocation(); }
    FVector GetPlayerRoomCenter() const { return FVector(0.0f, 0.0f, 200.0f); }
    
protected:
    virtual void BeginPlay() override;
    // Floor and ceiling
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Room|Structure")
    TObjectPtr<UStaticMeshComponent> FloorMesh;
    
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Room|Structure")
    TObjectPtr<UStaticMeshComponent> CeilingMesh;
    
    // Walls (front, back, left outer, right outer)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Room|Structure")
    TObjectPtr<UStaticMeshComponent> FrontWallMesh;
    
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Room|Structure")
    TObjectPtr<UStaticMeshComponent> BackWallMesh;
    
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Room|Structure")
    TObjectPtr<UStaticMeshComponent> LeftOuterWallMesh;
    
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Room|Structure")
    TObjectPtr<UStaticMeshComponent> RightOuterWallMesh;
    
    // Transparent partitions (dividing walls)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Room|Partitions")
    TObjectPtr<UStaticMeshComponent> LeftPartitionMesh;
    
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Room|Partitions")
    TObjectPtr<UStaticMeshComponent> RightPartitionMesh;
    
    // Room configuration (editable by humans in editor)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room Setup")
    float TotalRoomWidth = 1800.0f;  // 3 rooms total
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room Setup")
    float RoomDepth = 800.0f;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room Setup")
    float RoomHeight = 400.0f;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room Setup")
    float WallThickness = 10.0f;
    
    // Partition configuration
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room Setup", meta = (ClampMin = "0.0", ClampMax = "1.0"))
    float PartitionOpacity = 0.4f;
    
private:
    void ApplyTransparentMaterialToPartitions();
};
```


```cpp
// TrainingRoom.cpp
#include "TrainingRoom.h"
#include "Components/StaticMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Materials/MaterialInterface.h"

ATrainingRoom::ATrainingRoom()
{
    PrimaryActorTick.bCanEverTick = false;
    
    // Load project's LevelPrototyping meshes (better quality than engine basics)
    static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshAsset(
        TEXT("/Game/LevelPrototyping/Meshes/SM_Cube")
    );
    static ConstructorHelpers::FObjectFinder<UStaticMesh> PlaneMeshAsset(
        TEXT("/Game/LevelPrototyping/Meshes/SM_Plane")
    );
    
    // Load materials
    static ConstructorHelpers::FObjectFinder<UMaterialInterface> FloorMaterial(
        TEXT("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray")
    );
    static ConstructorHelpers::FObjectFinder<UMaterialInterface> WallMaterial(
        TEXT("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02")
    );
    static ConstructorHelpers::FObjectFinder<UMaterialInterface> CeilingMaterial(
        TEXT("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark")
    );
    
    // ===== FLOOR =====
    FloorMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Floor"));
    RootComponent = FloorMesh;
    
    if (CubeMeshAsset.Succeeded())
    {
        FloorMesh->SetStaticMesh(CubeMeshAsset.Object);
    }
    
    // Floor: 1800x800x10 cm (covers all 3 rooms)
    FloorMesh->SetRelativeScale3D(FVector(18.0f, 8.0f, 0.1f));
    FloorMesh->SetRelativeLocation(FVector::ZeroVector);
    
    // Apply material
    if (FloorMaterial.Succeeded())
    {
        FloorMesh->SetMaterial(0, FloorMaterial.Object);
    }
    
    // Set collision and mobility
    FloorMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
    FloorMesh->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
    FloorMesh->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
    FloorMesh->SetMobility(EComponentMobility::Static);
    
    // ===== CEILING =====
    CeilingMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Ceiling"));
    CeilingMesh->SetupAttachment(RootComponent);
    
    if (CubeMeshAsset.Succeeded())
    {
        CeilingMesh->SetStaticMesh(CubeMeshAsset.Object);
    }
    
    // Ceiling: 1800x800x10 cm at height 400
    CeilingMesh->SetRelativeScale3D(FVector(18.0f, 8.0f, 0.1f));
    CeilingMesh->SetRelativeLocation(FVector(0.0f, 0.0f, RoomHeight));
    CeilingMesh->SetMobility(EComponentMobility::Static);
    
    // Apply material
    if (CeilingMaterial.Succeeded())
    {
        CeilingMesh->SetMaterial(0, CeilingMaterial.Object);
    }
    
    // ===== FRONT WALL =====
    FrontWallMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("FrontWall"));
    FrontWallMesh->SetupAttachment(RootComponent);
    
    if (PlaneMeshAsset.Succeeded())
    {
        FrontWallMesh->SetStaticMesh(PlaneMeshAsset.Object);
    }
    
    // Front wall: 1800 wide x 400 high, at Y = 400 (front edge)
    FrontWallMesh->SetRelativeScale3D(FVector(18.0f, 4.0f, 1.0f));
    FrontWallMesh->SetRelativeLocation(FVector(0.0f, RoomDepth / 2.0f, RoomHeight / 2.0f));
    FrontWallMesh->SetRelativeRotation(FRotator(0.0f, 0.0f, 0.0f));
    FrontWallMesh->SetMobility(EComponentMobility::Static);
    
    // Apply material
    if (WallMaterial.Succeeded())
    {
        FrontWallMesh->SetMaterial(0, WallMaterial.Object);
    }
    
    // ===== BACK WALL =====
    BackWallMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BackWall"));
    BackWallMesh->SetupAttachment(RootComponent);
    
    if (PlaneMeshAsset.Succeeded())
    {
        BackWallMesh->SetStaticMesh(PlaneMeshAsset.Object);
    }
    
    // Back wall: 1800 wide x 400 high, at Y = -400 (back edge)
    BackWallMesh->SetRelativeScale3D(FVector(18.0f, 4.0f, 1.0f));
    BackWallMesh->SetRelativeLocation(FVector(0.0f, -RoomDepth / 2.0f, RoomHeight / 2.0f));
    BackWallMesh->SetRelativeRotation(FRotator(0.0f, 180.0f, 0.0f));
    BackWallMesh->SetMobility(EComponentMobility::Static);
    
    // Apply material
    if (WallMaterial.Succeeded())
    {
        BackWallMesh->SetMaterial(0, WallMaterial.Object);
    }
    
    // ===== LEFT OUTER WALL =====
    LeftOuterWallMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LeftOuterWall"));
    LeftOuterWallMesh->SetupAttachment(RootComponent);
    
    if (PlaneMeshAsset.Succeeded())
    {
        LeftOuterWallMesh->SetStaticMesh(PlaneMeshAsset.Object);
    }
    
    // Left outer wall: 800 deep x 400 high, at X = -900 (left edge)
    LeftOuterWallMesh->SetRelativeScale3D(FVector(8.0f, 4.0f, 1.0f));
    LeftOuterWallMesh->SetRelativeLocation(FVector(-TotalRoomWidth / 2.0f, 0.0f, RoomHeight / 2.0f));
    LeftOuterWallMesh->SetRelativeRotation(FRotator(0.0f, 90.0f, 0.0f));
    LeftOuterWallMesh->SetMobility(EComponentMobility::Static);
    
    // Apply material
    if (WallMaterial.Succeeded())
    {
        LeftOuterWallMesh->SetMaterial(0, WallMaterial.Object);
    }
    
    // ===== RIGHT OUTER WALL =====
    RightOuterWallMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RightOuterWall"));
    RightOuterWallMesh->SetupAttachment(RootComponent);
    
    if (PlaneMeshAsset.Succeeded())
    {
        RightOuterWallMesh->SetStaticMesh(PlaneMeshAsset.Object);
    }
    
    // Right outer wall: 800 deep x 400 high, at X = 900 (right edge)
    RightOuterWallMesh->SetRelativeScale3D(FVector(8.0f, 4.0f, 1.0f));
    RightOuterWallMesh->SetRelativeLocation(FVector(TotalRoomWidth / 2.0f, 0.0f, RoomHeight / 2.0f));
    RightOuterWallMesh->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
    RightOuterWallMesh->SetMobility(EComponentMobility::Static);
    
    // Apply material
    if (WallMaterial.Succeeded())
    {
        RightOuterWallMesh->SetMaterial(0, WallMaterial.Object);
    }
    
    // ===== LEFT TRANSPARENT PARTITION =====
    LeftPartitionMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LeftPartition"));
    LeftPartitionMesh->SetupAttachment(RootComponent);
    
    if (PlaneMeshAsset.Succeeded())
    {
        LeftPartitionMesh->SetStaticMesh(PlaneMeshAsset.Object);
    }
    
    // Left partition: 800 deep x 400 high, at X = -300 (between left and center rooms)
    constexpr float LeftPartitionX = -300.0f;
    LeftPartitionMesh->SetRelativeScale3D(FVector(8.0f, 4.0f, 1.0f));
    LeftPartitionMesh->SetRelativeLocation(FVector(LeftPartitionX, 0.0f, RoomHeight / 2.0f));
    LeftPartitionMesh->SetRelativeRotation(FRotator(0.0f, 90.0f, 0.0f));
    LeftPartitionMesh->SetMobility(EComponentMobility::Static);
    
    // Set collision (blocks movement but allows visibility)
    LeftPartitionMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
    LeftPartitionMesh->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
    LeftPartitionMesh->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
    
    // ===== RIGHT TRANSPARENT PARTITION =====
    RightPartitionMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RightPartition"));
    RightPartitionMesh->SetupAttachment(RootComponent);
    
    if (PlaneMeshAsset.Succeeded())
    {
        RightPartitionMesh->SetStaticMesh(PlaneMeshAsset.Object);
    }
    
    // Right partition: 800 deep x 400 high, at X = 300 (between center and right rooms)
    constexpr float RightPartitionX = 300.0f;
    RightPartitionMesh->SetRelativeScale3D(FVector(8.0f, 4.0f, 1.0f));
    RightPartitionMesh->SetRelativeLocation(FVector(RightPartitionX, 0.0f, RoomHeight / 2.0f));
    RightPartitionMesh->SetRelativeRotation(FRotator(0.0f, 90.0f, 0.0f));
    RightPartitionMesh->SetMobility(EComponentMobility::Static);
    
    // Set collision (blocks movement but allows visibility)
    RightPartitionMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
    RightPartitionMesh->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
    RightPartitionMesh->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
    
    UE_LOG(LogTemp, Display, TEXT("TrainingRoom created successfully via C++ code"));
}

void ATrainingRoom::BeginPlay()
{
    Super::BeginPlay();
    
    // Apply transparent material to partitions at runtime
    ApplyTransparentMaterialToPartitions();
}

void ATrainingRoom::ApplyTransparentMaterialToPartitions()
{
    // Load base material
    UMaterialInterface* BaseMaterial = LoadObject<UMaterialInterface>(
        nullptr,
        TEXT("/Game/LevelPrototyping/Materials/M_PrototypeGrid")
    );
    
    if (!BaseMaterial)
    {
        UE_LOG(LogTemp, Warning, TEXT("Failed to load base material for partitions"));
        return;
    }
    
    // Create dynamic material instance
    UMaterialInstanceDynamic* TransparentMaterial = UMaterialInstanceDynamic::Create(
        BaseMaterial,
        this
    );
    
    if (TransparentMaterial)
    {
        // Set transparency parameters
        TransparentMaterial->SetScalarParameterValue(TEXT("Opacity"), PartitionOpacity);
        TransparentMaterial->SetVectorParameterValue(
            TEXT("Color"), 
            FLinearColor(0.8f, 0.9f, 1.0f, PartitionOpacity)  // Light blue tint
        );
        
        // Apply to both partitions
        if (LeftPartitionMesh)
        {
            LeftPartitionMesh->SetMaterial(0, TransparentMaterial);
        }
        
        if (RightPartitionMesh)
        {
            RightPartitionMesh->SetMaterial(0, TransparentMaterial);
        }
        
        UE_LOG(LogTemp, Display, TEXT("Transparent partition materials applied successfully"));
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to create dynamic material instance for partitions"));
    }
}
```

**关键点：**
- 所有组件在构造函数中创建
- 使用项目的LevelPrototyping资源（网格和材质）
- 使用`ConstructorHelpers::FObjectFinder`加载项目资源
- 使用`constexpr`定义编译时常量
- 完整的碰撞设置
- 在BeginPlay中应用透明材质
- 无需任何编辑器操作

**使用的项目资源：**
- 网格：`/Game/LevelPrototyping/Meshes/SM_Cube`
- 网格：`/Game/LevelPrototyping/Meshes/SM_Plane`
- 材质：`/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray`（地板）
- 材质：`/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark`（天花板）
- 材质：`/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02`（墙壁）
- 材质：`/Game/LevelPrototyping/Materials/M_PrototypeGrid`（透明隔板基础材质）


### 2. AFPSTrainingGameMode

游戏模式，负责在运行时生成房间和管理游戏流程。

**UE5.7.0实现：**

```cpp
// FPSTrainingGameMode.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "FPSTrainingGameMode.generated.h"

// Forward declarations
class ATrainingRoom;

UCLASS()
class SHIJIEWUXIAN_API AFPSTrainingGameMode : public AGameModeBase
{
    GENERATED_BODY()
    
public:
    AFPSTrainingGameMode();
    
protected:
    virtual void BeginPlay() override;
    
    // Spawn the training room
    void SpawnTrainingRoom();
    
private:
    // Reference to spawned room
    UPROPERTY()
    TObjectPtr<ATrainingRoom> TrainingRoom;
    
    // Room spawn location
    UPROPERTY(EditDefaultsOnly, Category = "Room Setup")
    FVector RoomSpawnLocation = FVector::ZeroVector;
};
```

```cpp
// FPSTrainingGameMode.cpp
#include "FPSTrainingGameMode.h"
#include "TrainingRoom.h"
#include "Kismet/GameplayStatics.h"

AFPSTrainingGameMode::AFPSTrainingGameMode()
{
    // Set default pawn class to FirstPerson character
    // This will be set in editor or via DefaultGame.ini
}

void AFPSTrainingGameMode::BeginPlay()
{
    Super::BeginPlay();
    
    // Spawn the training room at runtime
    SpawnTrainingRoom();
    
    UE_LOG(LogTemp, Display, TEXT("FPSTrainingGameMode initialized"));
}

void AFPSTrainingGameMode::SpawnTrainingRoom()
{
    if (!GetWorld())
    {
        UE_LOG(LogTemp, Error, TEXT("World is null, cannot spawn training room"));
        return;
    }
    
    // Setup spawn parameters
    FActorSpawnParameters SpawnParams;
    SpawnParams.Owner = this;
    SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
    
    // Spawn the training room
    TrainingRoom = GetWorld()->SpawnActor<ATrainingRoom>(
        ATrainingRoom::StaticClass(),
        RoomSpawnLocation,
        FRotator::ZeroRotator,
        SpawnParams
    );
    
    if (TrainingRoom)
    {
        UE_LOG(LogTemp, Display, TEXT("Training room spawned successfully at %s"), 
               *RoomSpawnLocation.ToString());
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to spawn training room!"));
    }
}
```

**关键点：**
- 在`BeginPlay`中使用`SpawnActor`生成房间
- 使用`FActorSpawnParameters`配置生成行为
- 添加完整的错误检查和日志
- 无需在编辑器中手动放置房间


## Material Setup (Code-Based)

### Using Project Materials

项目中的LevelPrototyping材质包提供了高质量的原型材质：

**已应用的材质：**
- **地板**：`MI_PrototypeGrid_Gray` - 灰色网格材质
- **天花板**：`MI_PrototypeGrid_TopDark` - 深色网格材质
- **墙壁**：`MI_PrototypeGrid_Gray_02` - 浅灰色网格材质

### Transparent Partition Material

透明隔板需要半透明材质。实现方案：

**方案A：运行时创建动态材质实例（推荐）**
```cpp
// 在TrainingRoom.cpp的BeginPlay中
void ATrainingRoom::BeginPlay()
{
    Super::BeginPlay();
    
    // Load base material from project
    static ConstructorHelpers::FObjectFinder<UMaterialInterface> BaseMaterial(
        TEXT("/Game/LevelPrototyping/Materials/M_PrototypeGrid")
    );
    
    if (BaseMaterial.Succeeded())
    {
        // Create dynamic material instance for transparency
        UMaterialInstanceDynamic* TransparentMaterial = UMaterialInstanceDynamic::Create(
            BaseMaterial.Object, 
            this
        );
        
        if (TransparentMaterial)
        {
            // Set opacity (if material supports it)
            TransparentMaterial->SetScalarParameterValue(TEXT("Opacity"), PartitionOpacity);
            TransparentMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor(0.8f, 0.9f, 1.0f, 0.4f));
            
            LeftPartitionMesh->SetMaterial(0, TransparentMaterial);
            RightPartitionMesh->SetMaterial(0, TransparentMaterial);
            
            UE_LOG(LogTemp, Display, TEXT("Transparent partition materials applied"));
        }
    }
}
```

**方案B：使用项目现有材质（临时方案）**
```cpp
// 在构造函数中，先使用普通材质
static ConstructorHelpers::FObjectFinder<UMaterialInterface> PartitionMaterial(
    TEXT("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_Round")
);

if (PartitionMaterial.Succeeded())
{
    LeftPartitionMesh->SetMaterial(0, PartitionMaterial.Object);
    RightPartitionMesh->SetMaterial(0, PartitionMaterial.Object);
}
```

**推荐：方案A（动态材质实例）**
- 可以在运行时调整透明度
- 完全代码化，无需编辑器
- 人类可以后续创建专门的透明材质并替换

### Material Benefits

使用LevelPrototyping材质的优势：
- ✅ 高质量的网格纹理
- ✅ 统一的视觉风格
- ✅ 易于识别空间结构
- ✅ 适合原型开发和测试
- ✅ 人类可以后续替换为最终美术资源


## Player Setup (Code-Based)

### Using FirstPerson Template

项目已经有FirstPerson模板资源，直接使用即可。

**在GameMode中设置：**

```cpp
// FPSTrainingGameMode.cpp
#include "GameFramework/PlayerStart.h"

AFPSTrainingGameMode::AFPSTrainingGameMode()
{
    // Set default pawn class (FirstPerson character)
    // Option 1: Load from project's FirstPerson blueprint
    static ConstructorHelpers::FClassFinder<APawn> PlayerPawnBPClass(
        TEXT("/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter")
    );
    if (PlayerPawnBPClass.Class != nullptr)
    {
        DefaultPawnClass = PlayerPawnBPClass.Class;
    }
    
    // Set player controller class
    static ConstructorHelpers::FClassFinder<APlayerController> PlayerControllerBPClass(
        TEXT("/Game/FirstPerson/Blueprints/BP_FirstPersonPlayerController")
    );
    if (PlayerControllerBPClass.Class != nullptr)
    {
        PlayerControllerClass = PlayerControllerBPClass.Class;
    }
}

void AFPSTrainingGameMode::BeginPlay()
{
    Super::BeginPlay();
    
    // Spawn training room first
    SpawnTrainingRoom();
    
    // Spawn player start point in center room
    SpawnPlayerStartPoint();
}

void AFPSTrainingGameMode::SpawnPlayerStartPoint()
{
    if (!GetWorld())
    {
        return;
    }
    
    // Spawn PlayerStart in center of player room
    FActorSpawnParameters SpawnParams;
    SpawnParams.Owner = this;
    SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
    
    constexpr FVector PlayerStartLocation = FVector(0.0f, 0.0f, 100.0f);  // Center room, 100cm above floor
    constexpr FRotator PlayerStartRotation = FRotator(0.0f, 0.0f, 0.0f);  // Facing forward (+Y)
    
    APlayerStart* PlayerStart = GetWorld()->SpawnActor<APlayerStart>(
        APlayerStart::StaticClass(),
        PlayerStartLocation,
        PlayerStartRotation,
        SpawnParams
    );
    
    if (PlayerStart)
    {
        UE_LOG(LogTemp, Display, TEXT("PlayerStart spawned at center room"));
    }
    else
    {
        UE_LOG(LogTemp, Warning, TEXT("Failed to spawn PlayerStart, using default spawn"));
    }
}
```

**关键点：**
- 使用`ConstructorHelpers::FClassFinder`加载FirstPerson角色
- 在运行时生成PlayerStart
- 玩家自动出生在中间房间中心
- 完全代码化，无需编辑器操作


## Lighting Setup (Code-Based)

### Basic Lighting

可以通过代码添加基础照明。

```cpp
// In FPSTrainingGameMode.cpp
#include "Engine/DirectionalLight.h"
#include "Engine/PointLight.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/PointLightComponent.h"

void AFPSTrainingGameMode::SetupLighting()
{
    if (!GetWorld())
    {
        return;
    }
    
    FActorSpawnParameters SpawnParams;
    SpawnParams.Owner = this;
    SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
    
    // ===== DIRECTIONAL LIGHT (Sun) =====
    ADirectionalLight* SunLight = GetWorld()->SpawnActor<ADirectionalLight>(
        ADirectionalLight::StaticClass(),
        FVector::ZeroVector,
        FRotator(-45.0f, 45.0f, 0.0f),
        SpawnParams
    );
    
    if (SunLight && SunLight->GetLightComponent())
    {
        SunLight->GetLightComponent()->SetIntensity(3.0f);
        SunLight->GetLightComponent()->SetLightColor(FLinearColor::White);
        UE_LOG(LogTemp, Display, TEXT("Directional light created"));
    }
    
    // ===== POINT LIGHTS (Room lighting) =====
    // Left room light
    SpawnRoomLight(FVector(-600.0f, 0.0f, 350.0f));
    
    // Center room light (player room)
    SpawnRoomLight(FVector(0.0f, 0.0f, 350.0f));
    
    // Right room light
    SpawnRoomLight(FVector(600.0f, 0.0f, 350.0f));
}

void AFPSTrainingGameMode::SpawnRoomLight(const FVector& Location)
{
    if (!GetWorld())
    {
        return;
    }
    
    FActorSpawnParameters SpawnParams;
    SpawnParams.Owner = this;
    
    APointLight* RoomLight = GetWorld()->SpawnActor<APointLight>(
        APointLight::StaticClass(),
        Location,
        FRotator::ZeroRotator,
        SpawnParams
    );
    
    if (RoomLight && RoomLight->PointLightComponent)
    {
        RoomLight->PointLightComponent->SetIntensity(2000.0f);
        RoomLight->PointLightComponent->SetAttenuationRadius(1000.0f);
        RoomLight->PointLightComponent->SetLightColor(FLinearColor(1.0f, 0.95f, 0.9f));  // Warm white
        UE_LOG(LogTemp, Display, TEXT("Point light created at %s"), *Location.ToString());
    }
}
```

**在BeginPlay中调用：**
```cpp
void AFPSTrainingGameMode::BeginPlay()
{
    Super::BeginPlay();
    
    SpawnTrainingRoom();
    SpawnPlayerStartPoint();
    SetupLighting();  // Add lighting
}
```

**关键点：**
- 完全通过代码创建照明
- 1个定向光（太阳）+ 3个点光源（每个房间一个）
- 无需编辑器操作
- 人类可以后续在编辑器中调整光照参数


## Testing Checklist

完成代码后，验证以下功能：

### 编译和运行
- [ ] C++代码编译成功（无错误）
- [ ] 项目可以启动（PIE或Standalone）
- [ ] 无崩溃或严重警告

### 房间结构
- [ ] 3个房间正确生成（左、中、右）
- [ ] 房间尺寸正确（每个600x800x400 cm）
- [ ] 地板和天花板覆盖整个区域
- [ ] 所有墙壁正确放置

### 透明隔板
- [ ] 2个透明隔板正确放置（X = -300 和 X = +300）
- [ ] 隔板阻挡物理移动（玩家不能穿过）
- [ ] 可以通过隔板看到相邻房间（视觉穿透）

### 玩家功能
- [ ] 玩家正确出生在中间房间（X=0, Y=0, Z=100）
- [ ] 玩家可以使用第一人称视角
- [ ] 玩家可以在房间内自由移动
- [ ] 玩家不能穿过墙壁和隔板

### 照明
- [ ] 房间有充足的照明
- [ ] 可以清楚看到所有房间
- [ ] 透明隔板可见

### 日志输出
- [ ] 控制台显示"TrainingRoom created successfully"
- [ ] 控制台显示"Training room spawned successfully"
- [ ] 控制台显示"PlayerStart spawned"
- [ ] 控制台显示照明创建日志
- [ ] 无错误日志

## Implementation Workflow

### AI的工作流程（完全自动化）

1. **创建TrainingRoom类**
   - 创建`Source/shijiewuxian/TrainingRoom.h`
   - 创建`Source/shijiewuxian/TrainingRoom.cpp`
   - 在构造函数中创建所有组件

2. **创建/修改GameMode类**
   - 修改`AFPSTrainingGameMode`
   - 添加`SpawnTrainingRoom()`方法
   - 添加`SpawnPlayerStartPoint()`方法
   - 添加`SetupLighting()`方法

3. **编译项目**
   - 运行UBT编译C++代码
   - 检查编译错误

4. **测试运行**
   - 启动游戏（PIE或Standalone）
   - 验证房间正确生成
   - 验证玩家可以移动

5. **完成！**
   - AI的工作完成
   - 无需任何编辑器操作

### 人类的后续工作（可选）

人类可以在编辑器中：
1. 打开项目查看效果
2. 在Details面板调整房间参数（RoomWidth、RoomHeight等）
3. 创建自定义透明材质并替换
4. 调整照明强度和颜色
5. 添加装饰物和细节
6. 优化性能和视觉效果

**关键：AI完成所有核心功能，人类只做可选的美化工作。**

## Next Steps

完成房间搭建后，等待人类继续设计下功能（按优先级）：

1. **目标系统**：在白板区域生成可射击的目标球体
   - 设计文档：待创建

2. **统计系统**：追踪射击和命中数据，显示历史曲线
   - 设计文档：`.kiro/specs/fps-aim-trainer-stats/design.md`

3. **录像回放系统**：在对手房间回放历史录像
   - 设计文档：`.kiro/specs/fps-aim-trainer-replay/design.md`

每个功能都将使用相同的"AI完全代码化"方法实现。

