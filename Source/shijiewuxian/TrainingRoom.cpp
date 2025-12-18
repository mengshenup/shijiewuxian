// TrainingRoom.cpp
#include "TrainingRoom.h"
#include "Components/StaticMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Materials/MaterialInterface.h"
#include "Materials/MaterialInstanceDynamic.h"

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
	
	// Set collision and mobility
	CeilingMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	CeilingMesh->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
	CeilingMesh->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
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
	
	// Set collision and mobility
	FrontWallMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	FrontWallMesh->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
	FrontWallMesh->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
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
	
	// Set collision and mobility
	BackWallMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	BackWallMesh->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
	BackWallMesh->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
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
	
	// Set collision and mobility
	LeftOuterWallMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	LeftOuterWallMesh->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
	LeftOuterWallMesh->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
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
	
	// Set collision and mobility
	RightOuterWallMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	RightOuterWallMesh->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
	RightOuterWallMesh->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Block);
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
