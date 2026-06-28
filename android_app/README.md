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

The app reads the boat server URL from the Gradle property `boatServerUrl`.
If you do not provide it, the Android build defaults to:

```text
http://192.168.4.1:5000
```

To build for a Raspberry Pi at a different address:

```bash
./gradlew assembleDebug -PboatServerUrl=http://192.168.1.25:5000
```

You can also add this to `~/.gradle/gradle.properties` or the project `gradle.properties` file:

```properties
boatServerUrl=http://192.168.1.25:5000
```

## Testing Instructions

1. Open the `android_app` folder in Android Studio.
2. Let Android Studio sync Gradle.
3. Set `boatServerUrl` to the real Raspberry Pi Flask server URL, or use the default `http://192.168.4.1:5000`.
4. Run the app on an Android device or emulator.
5. Confirm the splash screen displays `Water Hyacinth Collection Boat` for 2 seconds.
6. Confirm the WebView opens the Raspberry Pi Flask dashboard.
7. Disconnect from Wi-Fi/mobile data and tap Retry.
8. Confirm the no-network message appears.
9. Reconnect to the Raspberry Pi network but stop the Flask server.
10. Tap Retry and confirm the server-offline message appears.

## Local Raspberry Pi Networks

The app only checks that Android is connected to Wi-Fi, cellular, or Ethernet. It does not require Android's `NET_CAPABILITY_INTERNET`, so it works when the phone is connected to a Raspberry Pi access point that has no outside internet access.

## Permissions

The manifest includes:

- `INTERNET`
- `ACCESS_NETWORK_STATE`

Cleartext HTTP traffic is enabled for local Raspberry Pi testing.
