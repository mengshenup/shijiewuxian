// FPSTrainingGameMode.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "FPSTrainingGameMode.generated.h"

// Forward declarations
class ATrainingRoom;
class APlayerStart;
class ADirectionalLight;
class APointLight;

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
	
	// Spawn player start point
	void SpawnPlayerStartPoint();
	
	// Setup lighting
	void SetupLighting();
	void SpawnRoomLight(const FVector& Location);
	
private:
	// Reference to spawned room
	UPROPERTY()
	TObjectPtr<ATrainingRoom> TrainingRoom;
	
	// Room spawn location
	UPROPERTY(EditDefaultsOnly, Category = "Room Setup")
	FVector RoomSpawnLocation = FVector::ZeroVector;
	
	// Lighting references
	UPROPERTY()
	TObjectPtr<ADirectionalLight> SunLight;
	
	UPROPERTY()
	TArray<TObjectPtr<APointLight>> RoomLights;
};
