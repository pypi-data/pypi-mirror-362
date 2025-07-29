#

from .jsc import fetch_methods_text, rps_dct, fetch_vals
def make_fcs(fc, add_src=True):
    def wfcs(codes, args, text):
        fcs, has_def = fetch_methods_text(codes, text)
        rst = []
        others = []
        if has_def:
            if add_src:
                rst.append(codes.rstrip())
            else:
                others.append(codes.rstrip())
        for _type, method, params in fcs:
            a, b = fc(_type, method, params, args)
            rst+=a
            others+=b
        return rst, others
    return wfcs