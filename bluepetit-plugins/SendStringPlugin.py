import time
import logging
from JoycontrolPlugin import JoycontrolPlugin, JoycontrolPluginError

logger = logging.getLogger(__name__)

class SendStringPlugin(JoycontrolPlugin):
    async def run(self):
        if self.options is None:
            raise JoycontrolPluginError('送信する文字列が必須です')

        self.base_time = 1 / 20
        self.press_time = self.base_time

        string = self.options[0].replace('\r\n', '\n')
        encoded_string = string.encode('utf-8')
        length = len(encoded_string)

        header = bytes.fromhex(f'00000000000000000000000000000000deadbeefdeadbeefdeadbeefb144{length:08x}')
        footer = bytes.fromhex(f'00000000000000000000000000000000')

        data = header + encoded_string + footer

        await self.send(data)

    async def send(self, data):
        buffer_length = 4

        for offset in range(0, len(data), buffer_length):
            start = time.perf_counter()

            buttons = []
            buttons.append('l_stick' if (offset // buffer_length) & 1 else 'r_stick')

            buttons.append('x') if (data[offset+0] >> 0) & 1 else None
            buttons.append('b') if (data[offset+0] >> 1) & 1 else None
            buttons.append('y') if (data[offset+0] >> 2) & 1 else None
            buttons.append('a') if (data[offset+0] >> 3) & 1 else None
            buttons.append('l') if (data[offset+0] >> 4) & 1 else None
            buttons.append('r') if (data[offset+0] >> 5) & 1 else None
            buttons.append('zl') if (data[offset+0] >> 6) & 1 else None
            buttons.append('zr') if (data[offset+0] >> 7) & 1 else None

            if data[offset+1] & 0x07 == 0x00:
                buttons.append('up')
            if data[offset+1] & 0x07 == 0x01:
                buttons.append('down')
            if data[offset+1] & 0x07 == 0x02:
                buttons.append('left')
            if data[offset+1] & 0x07 == 0x03:
                buttons.append('right')
            if data[offset+1] & 0x07 == 0x04:
                buttons.append('up')
                buttons.append('left')
            if data[offset+1] & 0x07 == 0x05:
                buttons.append('up')
                buttons.append('right')
            if data[offset+1] & 0x07 == 0x06:
                buttons.append('down')
                buttons.append('left')
            if data[offset+1] & 0x07 == 0x07:
                buttons.append('down')
                buttons.append('right')

            left_angle = data[offset+2] * 360 / 0x100
            right_angle = data[offset+3] * 360 / 0x100

            max_power = self.max_stick_power
            power_range = 0.9
            power_offset = 1.0 - power_range

            left_power = (float((data[offset+1] >> 3) & 0x03) / 0x04) * power_range + power_offset
            right_power = (float((data[offset+1] >> 5) & 0x07) / 0x09) * power_range + power_offset

            left_power = left_power * max_power
            right_power = right_power * max_power

            await self.left_stick(angle=left_angle, power=left_power)
            await self.right_stick(angle=right_angle, power=right_power)

            await self.button_push(*buttons, press_time_sec=self.press_time)

            end = time.perf_counter()
            self.press_time = self.base_time * self.base_time / (end - start)

            if self.press_time < 0:
                self.press_time = 0

        await self.left_stick('center')
        await self.right_stick('center')
