#!/usr/bin/env python3
import os
from pathlib import Path

FILES = {}

FILES["settings.gradle.kts"] = """pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name = "CardLink"
include(":app")
"""
FILES["build.gradle.kts"] = """plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
    id("com.google.devtools.ksp") version "1.9.24-1.0.20" apply false
    id("org.jetbrains.kotlin.plugin.serialization") version "1.9.24" apply false
}
"""
FILES["gradle.properties"] = "org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8\nandroid.useAndroidX=true\nkotlin.code.style=official\nandroid.nonTransitiveRClass=true"
FILES["app/proguard-rules.pro"] = "-keep class com.cardlink.app.data.model.** { *; }\n-keep class com.cardlink.app.util.** { *; }\n-keepattributes *Annotation*, InnerClasses, Signature\n-dontwarn com.google.zxing.**\n-dontwarn com.google.mlkit.**"

def main():
    for rel_path, content in FILES.items():
        path = Path(rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8")
    print("Project files created successfully.")

if __name__ == "__main__":
    main()
