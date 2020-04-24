import time
import numpy as np
import matplotlib
import visdom
import matplotlib.pyplot as plt
import torchvision
import os


def show_pic(img, ax):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
    img = img.transpose(1, 0, 2)
    ax.set_xlable("pic")
    return ax


class VISUAL():
    def __init__(self, env, **kwargs):
        self.vis = visdom.Visdom(env=env, **kwargs)
        self.kwargs = kwargs
        self.index = {}
        self.log_text = ''

    def reinit(self, env, **kwargs):
        self.vis = visdom.Visdom(env=env, **kwargs)
        return self

    def plot_all(self, d):
        for k, v in d.items():
            if v is not None:
                self.plot(k, v)

    def img_all(self, d):
        for k, v in d.items():
            self.img(k, v)

    def plot(self, name, y, **kwargs):
        x = self.index.get(name, 0)
        self.vis.line(X=np.array([x]), Y=np.array([y]),
                      win=name,
                      opts=dict(title=name),
                      update=None if x == 0 else 'append',
                      **kwargs)

    def img(self, t, name, img_, **kwargs):
        self.vis.imges(t.Tensor(img_).cpu().numpy(),
                       win=name,
                       opts=dict(title=name),
                       **kwargs)

    def log(self, info, win='log_text'):
        self.log_text += ('[{time}]{info}<br>'.format(
            time=time.strftime('%m%d_%H%M%S'),
            info=info
        ))
        self.vis.text(self.log_text, win)

    def __getattr__(self, name):
        return getattr(self.vis, name)

    def state_dict(self):
        return {
            'index': self.index,
            'vis_kwargs': self.kwargs,
            'log_text': self.log_text,
            'env': self.vis.env,
        }

    def load_state_dict(self, d):
        self.vis = visdom.Visdom(env=d.get('env', self.vis.env), **(self.d.get('vis_kw')))
        self.log_text = d.get('log_text')
        self.index = d.get('index', dict())
        return self


class PROCESS_IMG():
    def inverse_normalize(self, opt, img):
        if opt.caffe_pretrain:
            img = img.reshape(3, 1, 1)
            return img[::-1, :, :]
        return img.clip(0, 1) * 255

    def p_normalize(self, img):
        normalize = torchvision.transform.Normalize()
        img = normalize(img)
        return img.numpy()

    def c_normalize(self, img):
        img = img[[2, 1, 0], :, :]
        img = img * 255
        mean = np.array([11, 3.4, 5]).reshape(3, 1, 1)
        img = (img - mean).astype(np.float32, copy=True)
        return img

    def process(self, img, opt, min_size, max_size):
        C, H, W = img.shape
        scale1 = min_size / min(H, W)
        scale2 = max_size / max(H, W)
        scale = min(scale1, scale2)
        img = img / 255.

        if opt.caffe_pretrain:
            normalize = self.c_normalize()
        else:
            normalize = self.p_normalize()
        return normalize(img)


class Transform(object):

    def __init__(self, min_size=600, max_size=1000):
        self.min_size = min_size
        self.max_size = max_size

    def __call__(self, in_data, preprocess, util):
        img, bbox, label = in_data
        _, H, W = img.shape
        img = preprocess(img, self.min_size, self.max_size)
        _, o_H, o_W = img.shape
        scale = o_H / H
        bbox = util.resize_bbox(bbox, (H, W), (o_H, o_W))

        # horizontally flip
        img, params = util.random_flip(
            img, x_random=True, return_param=True)
        bbox = util.flip_bbox(
            bbox, (o_H, o_W), x_flip=params['x_flip'])

        return img, bbox, label, scale


class Dataset:
    def __init__(self, opt, VOCBboxDataset):
        self.opt = opt
        self.db = VOCBboxDataset(opt.voc_data_dir)
        self.tsf = Transform(opt.min_size, opt.max_size)

    def __getitem__(self, idx):
        ori_img, bbox, label, difficult = self.db.get_example(idx)
        img, bbox, label, scale = self.tsf((ori_img, bbox, label))
        return img.copy(), bbox.copy(), label.copy(), scale

    def __len__(self):
        return len(self.db)


class TestDataset:
    def __init__(self, opt, VOCBboxDataset, split='test', use_difficult=True):
        self.opt = opt
        self.db = VOCBboxDataset(opt.voc_data_dir, split=split, use_difficult=use_difficult)

    def __getitem__(self, idx):
        ori_img, bbox, label, difficult = self.db.get_example(idx)
        img = ori_img
        return img, ori_img.shape[1:], bbox, label, difficult

    def __len__(self):
        return len(self.db)


class VOCBboxDataset:

    def __init__(self, data_dir, split='trainval',
                 use_difficult=False, return_difficult=False,
                 ):

        id_list_file = os.path.join(
            data_dir, 'ImageSets/Main/{0}.txt'.format(split))

        self.ids = [id_.strip() for id_ in open(id_list_file)]
        self.data_dir = data_dir
        self.use_difficult = use_difficult
        self.return_difficult = return_difficult
        self.label_names = data_dir

    def __len__(self):
        return len(self.ids)

    def get_example(self, i, ET):
        id_ = self.ids[i]
        anno = ET.parse(
            os.path.join(self.data_dir, 'Annotations', id_ + '.xml'))
        bbox = list()
        label = list()
        difficult = list()
        for obj in anno.findall('object'):

            if not self.use_difficult and int(obj.find('difficult').text) == 1:
                continue

            difficult.append(int(obj.find('difficult').text))
            bndbox_anno = obj.find('bndbox')

            bbox.append([
                int(bndbox_anno.find(tag).text) - 1
                for tag in ('ymin', 'xmin', 'ymax', 'xmax')])
            name = obj.find('name').text.lower().strip()
            label.append(name)
        bbox = np.stack(bbox).astype(np.float32)
        label = np.stack(label).astype(np.int32)

        difficult = np.array(difficult, dtype=np.bool).astype(np.uint8)
        img_file = os.path.join(self.data_dir, 'JPEGImages', id_ + '.jpg')
        img = img_file
        return img, bbox, label, difficult

    __getitem__ = get_example


class PRO_IMG():
    def read_image(path, Image, dtype=np.float32, color=True):
        f = Image.open(path)
        try:
            if color:
                img = f.convert('RGB')
            else:
                img = f.convert('P')
            img = np.asarray(img, dtype=dtype)
        finally:
            if hasattr(f, 'close'):
                f.close()

        if img.ndim == 2:
            return img[np.newaxis]
        else:
            return img.transpose((2, 0, 1))

    def resize_bbox(bbox, in_size, out_size):
        bbox = bbox.copy()
        y_scale = float(out_size[0]) / in_size[0]
        x_scale = float(out_size[1]) / in_size[1]
        bbox[:, 0] = y_scale * bbox[:, 0]
        bbox[:, 2] = y_scale * bbox[:, 2]
        bbox[:, 1] = x_scale * bbox[:, 1]
        bbox[:, 3] = x_scale * bbox[:, 3]
        return bbox

    def flip_bbox(bbox, size, y_flip=False, x_flip=False):
        H, W = size
        bbox = bbox.copy()
        if y_flip:
            y_max = H - bbox[:, 0]
            y_min = H - bbox[:, 2]
            bbox[:, 0] = y_min
            bbox[:, 2] = y_max
        if x_flip:
            x_max = W - bbox[:, 1]
            x_min = W - bbox[:, 3]
            bbox[:, 1] = x_min
            bbox[:, 3] = x_max
        return bbox

    def crop_bbox(self,
                  bbox, y_slice=None, x_slice=None,
                  allow_outside_center=True, return_param=False):
        t, b = self._slice_to_bounds(y_slice)
        l, r = self._slice_to_bounds(x_slice)
        crop_bb = np.array((t, l, b, r))

        if allow_outside_center:
            mask = np.ones(bbox.shape[0], dtype=bool)
        else:
            center = (bbox[:, :2] + bbox[:, 2:]) / 2.0
            mask = np.logical_and(crop_bb[:2] <= center, center < crop_bb[2:]) \
                .all(axis=1)

        bbox = bbox.copy()
        bbox[:, :2] = np.maximum(bbox[:, :2], crop_bb[:2])
        bbox[:, 2:] = np.minimum(bbox[:, 2:], crop_bb[2:])
        bbox[:, :2] -= crop_bb[:2]
        bbox[:, 2:] -= crop_bb[:2]

        mask = np.logical_and(mask, (bbox[:, :2] < bbox[:, 2:]).all(axis=1))
        bbox = bbox[mask]

        if return_param:
            return bbox, {'index': np.flatnonzero(mask)}
        else:
            return bbox

    def _slice_to_bounds(slice_):
        if slice_ is None:
            return 0, np.inf

        if slice_.start is None:
            l = 0
        else:
            l = slice_.start

        if slice_.stop is None:
            u = np.inf
        else:
            u = slice_.stop

        return l, u

    def translate_bbox(bbox, y_offset=0, x_offset=0):
        out_bbox = bbox.copy()
        out_bbox[:, :2] += (y_offset, x_offset)
        out_bbox[:, 2:] += (y_offset, x_offset)

        return out_bbox

    def random_flip(img, random, y_random=False, x_random=False,
                    return_param=False, copy=False):
        y_flip, x_flip = False, False
        if y_random:
            y_flip = random.choice([True, False])
        if x_random:
            x_flip = random.choice([True, False])

        if y_flip:
            img = img[:, ::-1, :]
        if x_flip:
            img = img[:, :, ::-1]

        if copy:
            img = img.copy()

        if return_param:
            return img, {'y_flip': y_flip, 'x_flip': x_flip}
        else:
            return img
