// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class shijiewuxian : ModuleRules
{
	public shijiewuxian(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"shijiewuxian",
			"shijiewuxian/Variant_Horror",
			"shijiewuxian/Variant_Horror/UI",
			"shijiewuxian/Variant_Shooter",
			"shijiewuxian/Variant_Shooter/AI",
			"shijiewuxian/Variant_Shooter/UI",
			"shijiewuxian/Variant_Shooter/Weapons"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
