import numpy as np
from matplotlib import pyplot as plt

from fdhpy import (
    ChiouEtAl2025,
    KuehnEtAl2024,
    LavrentiadisAbrahamson2023,
    MossEtAl2024,
    MossRoss2011,
    PetersenEtAl2011,
    YoungsEtAl2003,
)

model = ChiouEtAl2025(magnitude=6.5, xl=0.25)
print(model.prob_exceed)

import fdhpy

print(fdhpy.__version__)


# params = model.stat_params_info["params"]
# print(params)
# ans = model.displ_avg
# print(ans)

# kwargs = {
# "magnitude": 7.0,
# # "xl": 0.33,
# "style": "reverse",
# "percentile": -1,
# "version": "full_coeffs",
# "use_girs": True,
# "folded": False,
# "metric": "sum-of-principal",
# "include_prob_zero": False,
# "folded": False,
# }

# model = KuehnEtAl2024(**kwargs)
# model.displ_profile

# fu = []
# model = KuehnEtAl2024(**kwargs)
# _xl = [0, 0.2, 0.4, 0.6, 0.8, 1]
# for x in _xl:
#     model.xl = x
#     fm = model._calc_fm()
#     mu = model.stat_params_info["params"]["u1"]["mu"]
#     _fu = mu - fm
#     fu.append(_fu)
# print(fu)

# fig, ax = plt.subplots(1, 1)
# ax.plot(_xl, fu)
# plt.show()

# model = ChiouEtAl2025(**kwargs)
# # print(model._calc_p_gap())
# # print(model._calc_p_zero_slip())
# for p in [0.05, 0.16, 0.5, 0.84, 0.95, -1]:
#     model.percentile = p
#     res = model.displ_site
#     print(np.round(res, 2))


# print(result.shape)
# # print(model.displ_site)
# np.savetxt("output.csv", result, delimiter=",", fmt="%f")

# mu = 0.884112258724909
# sigma = 0.3008697573436054
# pgap = 0.02015846999999998
# pzp = 0.01239160686043062

# s1 = np.random.normal(mu, sigma, 10_000)
# print(s1[0:10])
# s2 = np.where(s1 >= 0, s1, np.nan)
# s3 = np.nanmean(s2 ** (1 / 0.3))
# print(s3)
# print(s3 * (1 - pgap) * (1 - pzp))
