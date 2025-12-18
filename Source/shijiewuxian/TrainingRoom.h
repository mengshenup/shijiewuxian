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
