from source.util.settings import Settings
from source.util.database import Database
from source.util.timekeeper import Timestamps
import plotly.express as px
from PIL import Image as pil
import io
from dash import dcc, html


class Image:
    # Note: Avg image size at 352x288 is 56.7kb -> max nodes is 156 -> est. 38.75 Gb max of image data per year
    def __init__(self):
        self.config = Settings('general.config')
        self.db = Database(self.config.get_setting('databases', 'images_database_path'))
        self.ts = Timestamps()

    def validate_pixel_data(self, pixels):
        length = len(pixels)
        results = list()
        results.append(pixels[0] == 255)
        results.append(pixels[1] == 216)
        results.append(pixels[length-2] == 255)
        results.append(pixels[length-1] == 217)
        if False in results:
            return False
        return True

    def get_all_images(self):
        pass

    # def test_image(self):
    #     images = self.db.get_all()
    #     print(len(images))
    #     if images is None:
    #         return None
    #     image = images[-1]
    #     pixels = image['pixels']
    #     jpg = bytearray(pixels)
    #     buf = io.BytesIO(jpg)
    #     img = pil.open(buf)
    #     fig = px.imshow(img)
    #     fig.show()

    def get_test_image_div(self, node_id=None):
        if node_id is None:
            images = self.db.get_all()
        else:
            images = self.db.get_data_single_field('node_id', node_id)
        if len(images) < 1:
            return None
        print(len(images))
        if images is None:
            return None
        image = images[-1]
        pixels = image['pixels']
        jpg = bytearray(pixels)
        buf = io.BytesIO(jpg)
        img = pil.open(buf)
        width, height = img.size
        fig = px.imshow(img)
        title_div = html.Div([
            html.H2(str(node_id))
        ],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        date_taken = html.Div([
            html.P('Capture Date: ' + self.ts.get_time_date_string(image['timestamp']))
            ],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        size_div = html.Div([
            html.P('Resolution: {} x {} pixels'.format(width, height))
            ],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        divs = [title_div, date_taken, html.Br(), size_div, html.Br(), dcc.Graph(figure=fig)]
        # div = html.Div([
        #     html.H2(str(node_id)),
        #     html.Br(),
        #     dcc.Graph(figure=fig)
        #     ],
        #     style={'display': 'flex', 'justifyContent': 'center'}
        # )
        return divs

    def get_image_list(self, node_id):
        image_list = list()
        images = self.db.get_data_single_field('node_id', node_id)
        if len(images) < 1:
            return None
        print(len(images))
        images = sorted(images, key=lambda d: d['timestamp'], reverse=True)
        for image in images:
            image_string = str(image['node_id'])
            image_string += ' -> '
            image_string += self.ts.get_long_timestring(image['timestamp'])
            image_list.append(image_string)
        return image_list

    def get_image_div_with_timestring(self, timestring: str):
        try:
            timestring = timestring.split(' -> ')
            node_id = int(timestring[0])
            timestamp = self.ts.timestamp_from_long_timestring(timestring[1])
            dataobj = {
                'node_id': node_id,
                'timestamp': timestamp
            }
            image = self.db.get_data_from_obj(dataobj=dataobj)
            if image is None or len(image) < 1:
                return html.Div([])
            pixels = image[0]['pixels']
            jpg = bytearray(pixels)
            buf = io.BytesIO(jpg)
            img = pil.open(buf)
            fig = px.imshow(img)
            div = html.Div([
                dcc.Graph(figure=fig)
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'height': '50vh', 'width': '50vh'}
            )
        except Exception as e:
            print(e)
            return None
        return div


def main():
    img = Image()
    # img.test_image()


if __name__ == '__main__':
    main()

