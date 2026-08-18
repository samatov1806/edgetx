import os, re

# Determine path - running from edgetx source dir
src = 'radio/src/pulses/crossfire.cpp'
if not os.path.exists(src):
    # Try alternative path
    src = os.path.join(os.getcwd(), 'radio/src/pulses/crossfire.cpp')

with open(src, 'r') as f:
    content = f.read()

# 1. Add include after #include "crossfire.h"
content = content.replace(
    '#include "crossfire.h"',
    '#include "crossfire.h"\n#include "hal/usb_driver.h"', 1)

# 2. Add forwarding code after sendBuffer
content = content.replace(
    'drv->sendBuffer(drv_ctx, buffer, p_buf - buffer);',
    'drv->sendBuffer(drv_ctx, buffer, p_buf - buffer);\n\n  // Forward to USB VCP if Serial mode is active\n  if (usbPluggedInVCPMode()) {\n    auto usb_drv = UsbSerialPort.driver;\n    auto len = p_buf - buffer;\n    for (uint8_t i = 0; i < len; i++) {\n      usb_drv->sendByte(nullptr, buffer[i]);\n    }\n  }', 1)

with open(src, 'w') as f:
    f.write(content)
print('Patch applied OK')