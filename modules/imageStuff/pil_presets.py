from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageEnhance, ImageOps
from io import BytesIO
from datetime import datetime
from pilmoji import Pilmoji

from modules.imageStuff.writetext import WriteText


WHITE = (256, 256, 256)


def discord_quote(image: Image, username: str, ucolor: str, text: str):
    try:
        today = datetime.today()
        y = Image.new("RGBA", (2400, 800), (54, 57, 63))
        to_pa = image.resize((150, 150), 5)
        mask = Image.new("L", (150, 150), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0) + (150, 150), fill=255)
        avatar = ImageOps.fit(to_pa, mask.size, centering=(0.5, 0.5))
        y.paste(avatar, (50, 75), mask=mask)
        h = today.hour
        if h > 12:
            su = "PM"
            h = h - 12
        else:
            su = "AM"
        t_string = f"Today at {h}:{str(today.minute).zfill(2)} {su}"
        d = Pilmoji(y, use_microsoft_emoji=True)
        fntd = ImageFont.truetype("fonts/Whitney-Semibold.ttf", 60)
        fntt = ImageFont.truetype("fonts/Whitney-Medium.ttf", 35)
        user_color = WHITE
        d.text(
            (260, 70), username, fill=ucolor, font=fntd, emoji_position_offset=(0, 2)
        )
        wi = fntd.getsize(username)
        d.text((300 + wi[0], 92), t_string, fill=(114, 118, 125), font=fntt)
        wrap = WriteText(y)
        text_color = WHITE
        f = wrap.write_text_box(
            260,
            90,
            text[:1000],
            2120,
            "fonts/Whitney-Medium.ttf",
            50,
            color=text_color,
        )
        im = wrap.ret_img()
        ima = im.crop((0, 0, 2400, (f + 90)))
    finally:
        y.close()
        to_pa.close()
        mask.close()
        image.close()
        im.close()
    return ima


def whatwhat(img, top_text: str, bottom_text: str):
    try:
        im = img.convert("RGBA")
        im = im.resize((588, 488), resample=Image.BILINEAR)
        white_bg = Image.new("RGBA", (600, 500), (255, 255, 255))
        black_bg = Image.new("RGBA", (594, 494), (0, 0, 0))
        base = Image.new("RGBA", (800, 860), (0, 0, 0))
        white_bg.paste(black_bg, (3, 3), black_bg)
        white_bg.paste(im, (6, 6), im)
        base.paste(white_bg, (100, 100), white_bg)
        wt = WriteText(base)
        wt.write_text(
            "center",
            610,
            top_text,
            "fonts/times.ttf",
            "fill",
            600,
            100,
            (255, 255, 255),
        )
        wt.write_text(
            "center",
            720,
            bottom_text,
            "fonts/times.ttf",
            "fill",
            600,
            70,
            (255, 255, 255),
        )
        ret = wt.ret_img()
    finally:
        white_bg.close()
        black_bg.close()
        im.close()

    return ret
