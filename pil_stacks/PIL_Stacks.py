from typing import List, Dict, Union, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageEnhance
from pil_stacks.Layers import Layer, Text, Img, Color
from pil_stacks.Template import Template


class Stack(Template):
    def __init__(
        self,
        name: str,
        base: Union[str, Image.Image, Tuple[int, int]] = (0, 0),
        constant_base: bool = False,
        filters: Dict[str, float] = {
            "sharpness": 1.0,
            "contrast": 1.0,
            "color": 1.0,
            "brightness": 1.0,
        },
        template: str = None,
    ) -> None:
        self.name = name.replace(" ", "_")
        self.filters = filters
        if isinstance(base, str):
            self.image = Layer.open_image(base)
        elif isinstance(base, tuple):
            self.image = Color.create_blank(width=base[0], height=base[1])
        else:
            self.image = base

        self.layers: List[Union[Text, Img]] = []
        self.constant_base = constant_base

        if template is not None:
            self.import_template(template)

    def checklayer(self, layer) -> bool:
        return layer.name not in self.get_layer_names()

    def add_layer(self, layer: Union[Text, Img]) -> None:
        if self.checklayer(layer):
            self.layers.append(layer)

    def remove_layer(self, layer: Union[int, Union[Text, Img]]) -> None:
        if isinstance(layer, int):
            del self.layers[layer]
        else:
            self.layers.remove(layer)

    def swap_layer(self, index1: int, index2: int) -> None:
        self.layers[index1], self.layers[index2] = (
            self.layers[index2],
            self.layers[index1],
        )

    def insert_layer(self, layer: Union[Text, Img], index: int) -> None:
        if self.checklayer(layer):
            self.layers.insert(layer, index)

    def get_layer_names(self) -> List[str]:
        return [layer.name for layer in self.layers]

    def generate(self, **kwargs) -> Image.Image:
        result = self.image.copy()
        for layer in self.layers:
            if layer.constant is None:
                if layer.name in kwargs:
                    layer.draw(base=result, content=kwargs[layer.name])
            else:
                layer.draw(base=result)

        result = Layer.apply_filters(image=result, filters=self.filters)
        return result

    def save(self, fp: str, **kwargs) -> str:
        image = self.generate(**kwargs)
        image.save(fp)
