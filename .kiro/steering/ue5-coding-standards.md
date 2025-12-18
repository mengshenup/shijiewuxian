# Unreal Engine 5.7.0 C++ Coding Standards

## Project Info
- **Engine:** UE5.7.0 (Source Build at D:\UnrealEngine570)
- **C++ Standard:** C++20
- **Compiler:** MSVC 2022
- **Project:** shijiewuxian

## Mandatory UE5.7.0 API Requirements

### 1. Smart Pointers
**ALWAYS use `TObjectPtr<T>` for UObject pointers:**
```cpp
UPROPERTY()
TObjectPtr<UStaticMeshComponent> MeshComponent;
```

### 2. Enum Names
**ALWAYS use fully qualified enum names:**
```cpp
SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
```

### 3. Member Initialization
**ALWAYS initialize member variables inline (C++20):**
```cpp
float RoomWidth = 600.0f;
```

### 4. Compile-Time Constants
**Use `constexpr` for simple types, `const` for UE types:**
```cpp
constexpr float PartitionOffset = 300.0f;  // ✅ Simple type
const FVector Location = FVector(0, 0, 0); // ✅ UE type (NOT constexpr)
```

### 5. Actor Spawning
**ALWAYS use `FActorSpawnParameters`:**
```cpp
FActorSpawnParameters SpawnParams;
SpawnParams.Owner = this;
SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
GetWorld()->SpawnActor<AActor>(ActorClass, Location, Rotation, SpawnParams);
```

### 6. Static Constants
**Use engine-provided constants:**
```cpp
FVector::ZeroVector
FRotator::ZeroRotator
```

### 7. Forward Declarations
**ALWAYS use forward declarations in headers:**
```cpp
// Header
class UStaticMeshComponent;

// CPP
#include "Components/StaticMeshComponent.h"
```

### 8. UPROPERTY Specifiers
**ALWAYS include Category:**
```cpp
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room Setup")
float RoomWidth = 600.0f;

UPROPERTY(EditAnywhere, Category = "Settings", meta = (ClampMin = "0.0", ClampMax = "1.0"))
float Opacity = 0.4f;
```

### 9. Component Mobility
**Set mobility for static components:**
```cpp
MeshComponent->SetMobility(EComponentMobility::Static);
```

### 10. Logging
**Use UE_LOG for debugging:**
```cpp
UE_LOG(LogTemp, Warning, TEXT("Message: %s"), *Variable.ToString());
UE_LOG(LogTemp, Error, TEXT("Failed!"));
UE_LOG(LogTemp, Display, TEXT("Success"));
```

## Forbidden Patterns

❌ Raw pointers for UObjects: `UStaticMeshComponent* Mesh;`
❌ Short enum names: `ECC_WorldStatic`
❌ `constexpr` for UE types: `constexpr FVector Location`
❌ Missing error checks after SpawnActor
❌ Loading resources in constructor (use ConstructorHelpers)

## Map and Scene Generation

**Use Python scripts for map generation (Preferred):**

✅ Create Python scripts in `Scripts/MapGenerators/`
✅ Use UE5 Python API to generate maps and place Actors
✅ Script names match map names (e.g., `generate_map_name.py`)
✅ See `.kiro/steering/python-map-generation.md` for details

**C++ Actor Implementation:**

✅ Use `CreateDefaultSubobject` in constructors for components
✅ Use `ConstructorHelpers::FObjectFinder` for loading assets
✅ Set all transforms, materials, properties in code
✅ Actors can be placed in maps via Python scripts

❌ Do NOT manually place Actors in editor
❌ Do NOT create Blueprints for core functionality
❌ Do NOT use dynamic spawning in GameMode (use Python-generated maps instead)

**Humans CAN optionally adjust UPROPERTY values in editor after AI completes code.**

## Header Template
```cpp
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyActor.generated.h"

class UStaticMeshComponent;

UCLASS()
class SHIJIEWUXIAN_API AMyActor : public AActor
{
    GENERATED_BODY()
public:
    AMyActor();
protected:
    virtual void BeginPlay() override;
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    TObjectPtr<UStaticMeshComponent> MeshComponent;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Settings")
    float MyValue = 100.0f;
};
```

## Source Template
```cpp
#include "MyActor.h"
#include "Components/StaticMeshComponent.h"

AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = false;
    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    RootComponent = MeshComponent;
}

void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    UE_LOG(LogTemp, Display, TEXT("MyActor initialized"));
}
```

## Verification Checklist
- [ ] Using `TObjectPtr<T>` for all UObject pointers
- [ ] Using fully qualified enum names
- [ ] Initializing member variables inline
- [ ] Using `const` (not `constexpr`) for FVector/FRotator
- [ ] Using `FActorSpawnParameters` for spawning
- [ ] Using forward declarations in headers
- [ ] Including Category in UPROPERTY
- [ ] Adding error checks and logging
- [ ] Setting component mobility
- [ ] Creating all content in C++ code (no editor required)
