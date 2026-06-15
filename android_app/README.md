# Water Hyacinth Boat Android App - Phase 7

Android companion app built with Kotlin and WebView.

## Project Structure

```text
android_app/
|-- settings.gradle
|-- build.gradle
|-- app/
|   |-- build.gradle
|   `-- src/
|       `-- main/
|           |-- AndroidManifest.xml
|           |-- java/
|           |   `-- com/
|           |       `-- example/
|           |           `-- waterhyacinthboat/
|           |               |-- MainActivity.kt
|           |               `-- SplashActivity.kt
|           `-- res/
|               |-- drawable/
|               |   |-- ic_launcher.xml
|               |   `-- ic_launcher_round.xml
|               |-- layout/
|               |   |-- activity_main.xml
|               |   `-- activity_splash.xml
|               `-- values/
|                   |-- colors.xml
|                   |-- strings.xml
|                   `-- styles.xml
```

## Configure Raspberry Pi URL

Edit this line in `app/src/main/java/com/example/waterhyacinthboat/MainActivity.kt`:

```kotlin
private const val BOAT_SERVER_URL = "http://RASPBERRY_PI_IP"
```

Replace `RASPBERRY_PI_IP` with the Raspberry Pi address, for example:

```kotlin
private const val BOAT_SERVER_URL = "http://192.168.1.25:5000"
```

## Testing Instructions

1. Open the `android_app` folder in Android Studio.
2. Let Android Studio sync Gradle.
3. Replace `http://RASPBERRY_PI_IP` with the real Raspberry Pi Flask server URL.
4. Run the app on an Android device or emulator.
5. Confirm the splash screen displays `Water Hyacinth Collection Boat` for 2 seconds.
6. Confirm the WebView opens the Raspberry Pi Flask dashboard.
7. Turn off Wi-Fi/mobile data and tap Retry.
8. Confirm the no-internet message appears.
9. Reconnect to the network but stop the Flask server.
10. Tap Retry and confirm the server-offline message appears.

## Permissions

The manifest includes:

- `INTERNET`
- `ACCESS_NETWORK_STATE`

Cleartext HTTP traffic is enabled for local Raspberry Pi testing.
