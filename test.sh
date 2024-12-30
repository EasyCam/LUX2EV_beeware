export ANDROID_SDK_ROOT="/home/hadoop/.cache/briefcase/tools/android_sdk"
export PATH="$ANDROID_SDK_ROOT/cmdline-tools/12.0/bin:$PATH"
export JAVA_HOME="/home/hadoop/.cache/briefcase/tools/java17"
export PATH="$JAVA_HOME/bin:$PATH"

/home/hadoop/.cache/briefcase/tools/android_sdk/emulator/emulator "@beePhone" -dns-server 8.8.8.8   
/home/hadoop/.cache/briefcase/tools/android_sdk/emulator/emulator "@beePhone" -dns-server 8.8.8.8 -no-accel