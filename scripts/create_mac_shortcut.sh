#!/usr/bin/env bash
# Creates a macOS Desktop launcher for KCK Swap Shop with custom icon
# Run with: ./create_mac_shortcut.sh

set -euo pipefail

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

LAUNCHER_NAME="KCK Swap Shop.command"
DESKTOP_DIR="$HOME/Desktop"
LAUNCHER_PATH="$DESKTOP_DIR/$LAUNCHER_NAME"
ICON_PATH="$WORKSPACE_DIR/images/shortcut_logo.ico"

echo "========================================"
echo "  Creating macOS Desktop Launcher"
echo "========================================"
echo ""

# Create the launcher script
cat >"$LAUNCHER_PATH" <<EOF
#!/usr/bin/env bash
# KCK Swap Shop Launcher
set -euo pipefail

# Navigate to workspace
cd "$WORKSPACE_DIR"

# Make start.sh executable if needed
chmod +x start.sh

# Run the startup script
./start.sh
EOF

# Make it executable
chmod +x "$LAUNCHER_PATH"

echo "✓ Created launcher: $LAUNCHER_PATH"

# Set custom icon if the icon file exists
if [ -f "$ICON_PATH" ]; then
    echo "✓ Found icon: $ICON_PATH"
    
    # Convert ICO to ICNS format using sips
    TEMP_ICNS="/tmp/kck_swap_shop_icon.icns"
    
    if command -v sips >/dev/null 2>&1; then
        echo "Converting ICO to ICNS format..."
        
        # Create iconset folder
        ICONSET_DIR="/tmp/kck_icon.iconset"
        mkdir -p "$ICONSET_DIR"
        
        # Generate different sizes for the iconset from ICO
        sips -z 16 16     "$ICON_PATH" --out "$ICONSET_DIR/icon_16x16.png" >/dev/null 2>&1
        sips -z 32 32     "$ICON_PATH" --out "$ICONSET_DIR/icon_16x16@2x.png" >/dev/null 2>&1
        sips -z 32 32     "$ICON_PATH" --out "$ICONSET_DIR/icon_32x32.png" >/dev/null 2>&1
        sips -z 64 64     "$ICON_PATH" --out "$ICONSET_DIR/icon_32x32@2x.png" >/dev/null 2>&1
        sips -z 128 128   "$ICON_PATH" --out "$ICONSET_DIR/icon_128x128.png" >/dev/null 2>&1
        sips -z 256 256   "$ICON_PATH" --out "$ICONSET_DIR/icon_128x128@2x.png" >/dev/null 2>&1
        sips -z 256 256   "$ICON_PATH" --out "$ICONSET_DIR/icon_256x256.png" >/dev/null 2>&1
        sips -z 512 512   "$ICON_PATH" --out "$ICONSET_DIR/icon_256x256@2x.png" >/dev/null 2>&1
        sips -z 512 512   "$ICON_PATH" --out "$ICONSET_DIR/icon_512x512.png" >/dev/null 2>&1
        
        # Convert iconset to ICNS
        iconutil -c icns "$ICONSET_DIR" -o "$TEMP_ICNS" >/dev/null 2>&1
        
        # Apply icon to the launcher using AppleScript
        osascript <<APPLESCRIPT
use framework "Foundation"
use framework "AppKit"

-- Read icon file
set iconImage to current application's NSImage's alloc()'s initWithContentsOfFile:"$TEMP_ICNS"

-- Get launcher file
set launcherPath to "$LAUNCHER_PATH"
set workspace to current application's NSWorkspace's sharedWorkspace()

-- Set icon
workspace's setIcon:iconImage forFile:launcherPath options:0

return "Icon set successfully"
APPLESCRIPT
        
        # Cleanup
        rm -rf "$ICONSET_DIR" "$TEMP_ICNS"
        
        echo "✓ Icon applied successfully!"
    else
        echo "⚠ sips command not found, skipping icon conversion"
    fi
else
    echo "⚠ Icon file not found at: $ICON_PATH"
    echo "  Launcher created without custom icon"
fi

echo ""
echo "========================================"
echo "  Done!"
echo "========================================"
echo ""
echo "Double-click '$LAUNCHER_NAME' on your Desktop to launch."
echo ""
