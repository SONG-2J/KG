# 使用globalpointer预测
from ere.rel.globalpointer_re import *


def get_spo(text):
    model.load_weights(model_save_path)
    R = set([SPO(spo) for spo in extract_spoes(text)])
    print(text)
    print(R)


if __name__ == '__main__':
    get_spo("一种便携式双波段UV LED杀菌消毒灯，包括双波段UV LED灯珠的铝基灯板、包裹所述铝基灯板的散热片及网格铁艺面罩，所述双波段UV LED灯珠内设有波长为395～420nm的UVA芯片和波长为255～285nm的UVC芯片")
