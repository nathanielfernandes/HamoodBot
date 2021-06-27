from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageEnhance, ImageOps
from io import BytesIO
from datetime import datetime
from pilmoji import Pilmoji
import re, math

from modules.imageStuff.writetext import WriteText

WHITE = (256, 256, 256)

EMOJI = re.compile(r"(<a?:\w+:?\d+>)")


def standardize(image: Image, _max=1000, _min=500):
    w, h = image.size
    m = max(w, h)
    mm = min(w, h)
    if m > _max:
        s = _max / m
    elif mm < _min:
        s = _min / mm
    else:
        s = 1

    return image.resize((round(w * s), round(h * s)), Image.ANTIALIAS)


def standardmeme(image, toptext, bottomtext):
    image = image.convert("RGBA")
    image = standardize(image)

    w, h = image.size
    mw, mh = w - 10, round(h / 6)

    wt = WriteText(image)
    try:
        if toptext != "":
            wt.write_text(
                "center",
                0,
                toptext[:40],
                "fonts/impact.ttf",
                "fill",
                mw,
                mh,
                (255, 255, 255),
            )
        fs = wt.get_font_size(bottomtext[:40], "fonts/impact.ttf", mw, mh)
        y2 = wt.get_text_size("fonts/impact.ttf", fs, bottomtext[:40])
        wt.write_text(
            "center",
            h - y2[1] - 10,
            bottomtext[:40],
            "fonts/impact.ttf",
            "fill",
            mw,
            mh,
            (255, 255, 255),
        )
    except Exception as e:
        raise e
        ret = None
    else:
        ret = wt.ret_img()

    return ret


def rainbowfy(image):
    try:
        image = image.convert("RGBA")
        image = standardize(image)
        w, h = image.size
        r = Image.open("memePics/lgbtImage.png")
        r = r.resize((w, h))
        image.paste(r, (0, 0), mask=r)
        image.paste(r, (0, 0), mask=r)
    finally:
        r.close()
    return image


def betterText(text, font, color):
    with Image.new("RGBA", (0, 0), (0, 0, 0, 0)) as placeholder:
        pdraw = ImageDraw.Draw(placeholder)
        all_es = EMOJI.findall(text)
        nt = str(text)
        for e in all_es:
            nt = nt.replace(e, "O")
        w, h = pdraw.textsize(nt, font)
        with Image.new("RGBA", (w + 40, h + 30), (0, 0, 0, 0)) as img:
            with Pilmoji(img) as pilmoji:
                pilmoji.text(
                    xy=(10, 10),
                    text=text,
                    fill=color,
                    font=font,
                    anchor=None,
                    spacing=0,
                    align="left",
                    emoji_size_factor=0.8,
                )
    return img


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


ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "][::-1]


def regulate_size(image, scale=100):
    w, h = image.size
    r = h / w
    height_f = int(scale * r)
    return image.resize((int(scale * 1.75), height_f))


def image_grayscale(image):
    return image.convert("L")


def image_to_ascii(image=None, scale=None):
    image = regulate_size(image)
    x, y = image.size
    if x * y > 1990:
        s = math.sqrt(1990 / (x * y))
        image = image.resize((int(x * s), int(y * s)))

    image = image_grayscale(image)

    if scale is None:
        scale = image.size[0]

    pixels = image.getdata()

    ascii_pixels = "".join([ASCII_CHARS[p // 25] for p in pixels])
    return "\n".join(
        ascii_pixels[i : (i + scale)] for i in range(0, len(ascii_pixels), scale)
    )
