#!/usr/bin/env python3
"""
CardLink – Smart Digital Business Card
Complete Android Project Generator for GitHub Actions & Local Builds.
"""

import os
from pathlib import Path

FILES = {}

# ==============================================================================
# 1. ROOT GRADLE & CONFIGURATION FILES
# ==============================================================================

FILES["settings.gradle.kts"] = """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
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

FILES["gradle.properties"] = """org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
"""

FILES["app/proguard-rules.pro"] = """-keep class com.cardlink.app.data.model.** { *; }
-keep class com.cardlink.app.util.** { *; }
-keepattributes *Annotation*, InnerClasses, Signature
-dontwarn com.google.zxing.**
-dontwarn com.google.mlkit.**
"""

# ==============================================================================
# 2. APP MODULE BUILD.GRADLE.KTS (WITH AUTO RELEASE SIGNING)
# ==============================================================================

FILES["app/build.gradle.kts"] = """import java.io.File

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.devtools.ksp")
    id("org.jetbrains.kotlin.plugin.serialization")
}

android {
    namespace = "com.cardlink.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.cardlink.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        vectorDrawables { useSupportLibrary = true }
    }

    signingConfigs {
        create("release") {
            val ksFile = rootProject.file("cardlink-release.jks")
            if (ksFile.exists()) {
                storeFile = ksFile
                storePassword = "cardlink123"
                keyAlias = "cardlink"
                keyPassword = "cardlink123"
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            val ksFile = rootProject.file("cardlink-release.jks")
            if (ksFile.exists()) {
                signingConfig = signingConfigs.getByName("release")
            } else {
                signingConfig = signingConfigs.getByName("debug")
            }
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.06.00"))
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-compose:1.9.1")
    implementation("androidx.fragment:fragment-ktx:1.8.2")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.navigation:navigation-compose:2.7.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.4")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.4")

    // Room Local Database
    val roomVersion = "2.6.1"
    implementation("androidx.room:room-runtime:$roomVersion")
    implementation("androidx.room:room-ktx:$roomVersion")
    ksp("androidx.room:room-compiler:$roomVersion")

    // DataStore & Serialization
    implementation("androidx.datastore:datastore-preferences:1.1.1")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")

    // Google Nearby Connections (Bluetooth / Wi-Fi Direct P2P)
    implementation("com.google.android.gms:play-services-nearby:19.3.0")

    // QR Generation (ZXing) + ML Kit Barcode & Text OCR + CameraX
    implementation("com.google.zxing:core:3.5.3")
    implementation("com.google.mlkit:barcode-scanning:17.2.0")
    implementation("com.google.mlkit:text-recognition:16.0.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.8.1")

    val cameraVersion = "1.3.4"
    implementation("androidx.camera:camera-core:$cameraVersion")
    implementation("androidx.camera:camera-camera2:$cameraVersion")
    implementation("androidx.camera:camera-lifecycle:$cameraVersion")
    implementation("androidx.camera:camera-view:$cameraVersion")

    // Coil Image Loader
    implementation("io.coil-kt:coil-compose:2.6.0")

    // Jetpack Glance Home Screen Widget
    implementation("androidx.glance:glance-appwidget:1.1.0")
    implementation("androidx.glance:glance-material3:1.1.0")
}
"""

# ==============================================================================
# 3. ANDROID MANIFEST & XML RESOURCES
# ==============================================================================

FILES["app/src/main/AndroidManifest.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- NFC -->
    <uses-permission android:name="android.permission.NFC" />
    <uses-feature android:name="android.hardware.nfc" android:required="false" />
    <uses-feature android:name="android.hardware.nfc.hce" android:required="false" />

    <!-- Bluetooth & Nearby Connections -->
    <uses-permission android:name="android.permission.BLUETOOTH" android:maxSdkVersion="30" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" android:maxSdkVersion="30" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADVERTISE" android:usesPermissionFlags="neverForLocation" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" android:usesPermissionFlags="neverForLocation" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" android:usesPermissionFlags="neverForLocation" />
    <uses-permission android:name="android.permission.NEARBY_WIFI_DEVICES" android:usesPermissionFlags="neverForLocation" />

    <!-- Camera & Contacts -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera.any" android:required="false" />
    <uses-permission android:name="android.permission.WRITE_CONTACTS" />

    <queries>
        <package android:name="com.whatsapp" />
        <package android:name="com.whatsapp.w4b" />
        <package android:name="com.google.android.apps.maps" />
        <intent>
            <action android:name="android.intent.action.DIAL" />
            <data android:scheme="tel" />
        </intent>
        <intent>
            <action android:name="android.intent.action.SENDTO" />
            <data android:scheme="mailto" />
        </intent>
        <intent>
            <action android:name="android.intent.action.VIEW" />
            <data android:scheme="https" />
        </intent>
    </queries>

    <application
        android:allowBackup="true"
        android:icon="@drawable/ic_launcher_cardlink"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.CardLink">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.nfc.action.NDEF_DISCOVERED" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="text/x-vcard" />
            </intent-filter>
        </activity>

        <!-- NFC Host Card Emulation Service -->
        <service
            android:name=".nfc.CardLinkHceService"
            android:exported="true"
            android:permission="android.permission.BIND_NFC_SERVICE">
            <intent-filter>
                <action android:name="android.nfc.cardemulation.action.HOST_APDU_SERVICE" />
            </intent-filter>
            <meta-data
                android:name="android.nfc.cardemulation.host_apdu_service"
                android:resource="@xml/apduservice" />
        </service>

        <!-- Quick Settings Tile Service -->
        <service
            android:name=".tile.CardLinkTileService"
            android:exported="true"
            android:icon="@drawable/ic_qs_cardlink"
            android:label="CardLink Share"
            android:permission="android.permission.BIND_QUICK_SETTINGS_TILE">
            <intent-filter>
                <action android:name="android.service.quicksettings.action.QS_TILE" />
            </intent-filter>
        </service>

        <!-- Home Screen Glance AppWidget -->
        <receiver
            android:name=".widget.CardLinkWidgetReceiver"
            android:exported="true"
            android:label="CardLink Executive QR Widget">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/cardlink_widget_info" />
        </receiver>

        <!-- FileProvider for .vcf, .png, and .pdf sharing -->
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
"""

FILES["app/src/main/res/values/strings.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">CardLink</string>
</resources>
"""

FILES["app/src/main/res/values/themes.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.CardLink" parent="android:Theme.Material.Light.NoActionBar" />
</resources>
"""

FILES["app/src/main/res/xml/apduservice.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<host-apdu-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:description="@string/app_name"
    android:requireDeviceUnlock="false">
    <aid-group android:description="@string/app_name" android:category="other">
        <aid-filter android:name="D2760000850101" />
        <aid-filter android:name="F0434152444C494E4B" />
    </aid-group>
</host-apdu-service>
"""

FILES["app/src/main/res/xml/file_paths.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<paths>
    <cache-path name="shared_cards" path="cards/" />
    <files-path name="scanned_cards" path="scanned_cards/" />
</paths>
"""

FILES["app/src/main/res/xml/cardlink_widget_info.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="250dp"
    android:minHeight="140dp"
    android:resizeMode="horizontal|vertical"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/widget_loading"
    android:description="@string/app_name"
    android:widgetCategory="home_screen" />
"""

FILES["app/src/main/res/layout/widget_loading.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#0A192F"
    android:padding="16dp">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="center"
        android:text="CardLink QR Ready"
        android:textColor="#D4AF37"
        android:textStyle="bold" />
</FrameLayout>
"""

FILES["app/src/main/res/drawable/ic_qs_cardlink.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24"
    android:tint="#FFFFFF">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M20,4H4C2.9,4 2,4.9 2,6v12c0,1.1 0.9,2 2,2h16c1.1,0 2,-0.9 2,-2V6C22,4.9 21.1,4 20,4zM20,18H4V6h16V18zM6,10h2v2H6V10zM6,14h8v2H6V14z" />
</vector>
"""

FILES["app/src/main/res/drawable/ic_launcher_cardlink.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0A192F"
        android:pathData="M0,0h108v108h-108z" />
    <path
        android:fillColor="#D4AF37"
        android:pathData="M24,32h60c3.3,0 6,2.7 6,6v32c0,3.3 -2.7,6 -6,6H24c-3.3,0 -6,-2.7 -6,-6V38C18,34.7 20.7,32 24,32z" />
    <path
        android:fillColor="#0A192F"
        android:pathData="M28,44h28v5H28zM28,54h42v4H28zM28,62h20v4H28z" />
</vector>
"""

# ==============================================================================
# 4. KOTLIN SOURCE CODE: DATA MODELS & ROOM DATABASE
# ==============================================================================

FILES["app/src/main/java/com/cardlink/app/data/model/Entities.kt"] = """package com.cardlink.app.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import kotlinx.serialization.Serializable

enum class CardTemplate {
    EXECUTIVE_NAVY, MINIMAL_IVORY, CHARCOAL_GOLD, MODERN_SPLIT
}

@Serializable
@Entity(tableName = "my_cards")
data class BusinessCardEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val profileTitle: String = "Corporate",
    val isDefault: Boolean = true,
    val fullName: String = "",
    val designation: String = "",
    val companyName: String = "",
    val department: String = "",
    val bio: String = "",
    val phone: String = "",
    val whatsapp: String = "",
    val email: String = "",
    val officeAddress: String = "",
    val website: String = "",
    val linkedInUrl: String = "",
    val facebookUrl: String = "",
    val otherSocialUrl: String = "",
    val profilePhotoUri: String? = null,
    val companyLogoUri: String? = null,
    val template: CardTemplate = CardTemplate.EXECUTIVE_NAVY,
    val primaryColorHex: Long = 0xFF0A192F,
    val accentColorHex: Long = 0xFFD4AF37,
    val textColorHex: Long = 0xFFFFFFFF,
    val fontFamilyName: String = "Serif",
    val cornerRadiusDp: Int = 16,
    val sharePhone: Boolean = true,
    val shareWhatsapp: Boolean = true,
    val shareEmail: Boolean = true,
    val shareAddress: Boolean = true,
    val shareSocials: Boolean = true
) {
    fun sanitizedForSharing(): BusinessCardEntity = copy(
        phone = if (sharePhone) phone else "",
        whatsapp = if (shareWhatsapp) whatsapp else "",
        email = if (shareEmail) email else "",
        officeAddress = if (shareAddress) officeAddress else "",
        linkedInUrl = if (shareSocials) linkedInUrl else "",
        facebookUrl = if (shareSocials) facebookUrl else "",
        otherSocialUrl = if (shareSocials) otherSocialUrl else "",
        profilePhotoUri = null,
        companyLogoUri = null
    )
}

@Serializable
@Entity(tableName = "saved_contacts")
data class SavedContactEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val fullName: String,
    val designation: String = "",
    val companyName: String = "",
    val department: String = "",
    val bio: String = "",
    val phone: String = "",
    val whatsapp: String = "",
    val email: String = "",
    val officeAddress: String = "",
    val website: String = "",
    val linkedInUrl: String = "",
    val facebookUrl: String = "",
    val otherSocialUrl: String = "",
    val profilePhotoUri: String? = null,
    val notes: String = "",
    val receivedVia: String = "QR Code",
    val savedAtTimestamp: Long = System.currentTimeMillis()
)

@Entity(tableName = "share_history")
data class ShareHistoryEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val cardProfileTitle: String,
    val method: String,
    val recipientInfo: String,
    val timestamp: Long = System.currentTimeMillis()
)
"""

FILES["app/src/main/java/com/cardlink/app/data/local/CardLinkDatabase.kt"] = """package com.cardlink.app.data.local

import android.content.Context
import androidx.room.*
import com.cardlink.app.data.model.*
import kotlinx.coroutines.flow.Flow

@Dao
interface CardLinkDao {
    @Query("SELECT * FROM my_cards ORDER BY isDefault DESC, id ASC")
    fun getAllMyCards(): Flow<List<BusinessCardEntity>>

    @Query("SELECT * FROM my_cards ORDER BY id ASC")
    suspend fun getAllMyCardsSnapshot(): List<BusinessCardEntity>

    @Query("SELECT * FROM my_cards WHERE isDefault = 1 LIMIT 1")
    suspend fun getDefaultCardSnapshot(): BusinessCardEntity?

    @Upsert
    suspend fun upsertMyCard(card: BusinessCardEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertMyCardsBatch(cards: List<BusinessCardEntity>)

    @Query("UPDATE my_cards SET isDefault = CASE WHEN id = :cardId THEN 1 ELSE 0 END")
    suspend fun setActiveCard(cardId: Long)

    @Query("DELETE FROM my_cards")
    suspend fun clearAllMyCards()

    @Query(\"\"\"
        SELECT * FROM saved_contacts 
        WHERE fullName LIKE '%' || :query || '%' 
           OR companyName LIKE '%' || :query || '%' 
           OR designation LIKE '%' || :query || '%'
           OR notes LIKE '%' || :query || '%'
        ORDER BY savedAtTimestamp DESC
    \"\"\")
    fun searchContacts(query: String): Flow<List<SavedContactEntity>>

    @Query("SELECT * FROM saved_contacts ORDER BY savedAtTimestamp DESC")
    suspend fun getAllContactsSnapshot(): List<SavedContactEntity>

    @Upsert
    suspend fun upsertContact(contact: SavedContactEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertContactsBatch(contacts: List<SavedContactEntity>)

    @Delete
    suspend fun deleteContact(contact: SavedContactEntity)

    @Query("DELETE FROM saved_contacts")
    suspend fun clearAllContacts()

    @Insert
    suspend fun logShareEvent(event: ShareHistoryEntity)

    @Query("SELECT * FROM share_history ORDER BY timestamp DESC LIMIT 50")
    fun getShareHistory(): Flow<List<ShareHistoryEntity>>
}

@Database(
    entities = [BusinessCardEntity::class, SavedContactEntity::class, ShareHistoryEntity::class],
    version = 1,
    exportSchema = false
)
abstract class CardLinkDatabase : RoomDatabase() {
    abstract fun dao(): CardLinkDao

    companion object {
        @Volatile
