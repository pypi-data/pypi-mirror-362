"""PartAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results import _2894

_PART_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "PartAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7392,
        _7393,
        _7394,
        _7399,
        _7401,
        _7402,
        _7403,
        _7405,
        _7406,
        _7408,
        _7409,
        _7410,
        _7411,
        _7413,
        _7414,
        _7415,
        _7416,
        _7418,
        _7420,
        _7421,
        _7423,
        _7424,
        _7426,
        _7427,
        _7429,
        _7431,
        _7433,
        _7435,
        _7436,
        _7438,
        _7439,
        _7440,
        _7443,
        _7445,
        _7447,
        _7448,
        _7449,
        _7450,
        _7452,
        _7453,
        _7454,
        _7455,
        _7457,
        _7458,
        _7459,
        _7461,
        _7463,
        _7465,
        _7466,
        _7468,
        _7469,
        _7471,
        _7473,
        _7474,
        _7475,
        _7476,
        _7477,
        _7478,
        _7479,
        _7480,
        _7482,
        _7484,
        _7485,
        _7486,
        _7487,
        _7488,
        _7489,
        _7491,
        _7492,
        _7494,
        _7495,
        _7496,
        _7498,
        _7499,
        _7501,
        _7502,
        _7504,
        _7505,
        _7507,
        _7508,
        _7510,
        _7511,
        _7512,
        _7513,
        _7514,
        _7515,
        _7516,
        _7517,
        _7519,
        _7520,
        _7522,
        _7523,
        _7524,
        _7526,
        _7527,
        _7529,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7124,
        _7125,
        _7126,
        _7132,
        _7134,
        _7135,
        _7137,
        _7139,
        _7140,
        _7142,
        _7143,
        _7144,
        _7145,
        _7147,
        _7148,
        _7149,
        _7150,
        _7152,
        _7154,
        _7155,
        _7157,
        _7158,
        _7160,
        _7161,
        _7163,
        _7165,
        _7166,
        _7168,
        _7169,
        _7171,
        _7172,
        _7173,
        _7176,
        _7178,
        _7179,
        _7180,
        _7181,
        _7182,
        _7184,
        _7185,
        _7186,
        _7187,
        _7189,
        _7190,
        _7192,
        _7194,
        _7196,
        _7198,
        _7199,
        _7201,
        _7202,
        _7204,
        _7205,
        _7206,
        _7207,
        _7208,
        _7209,
        _7210,
        _7211,
        _7212,
        _7214,
        _7216,
        _7217,
        _7218,
        _7219,
        _7220,
        _7221,
        _7223,
        _7224,
        _7226,
        _7227,
        _7228,
        _7230,
        _7231,
        _7233,
        _7234,
        _7236,
        _7237,
        _7239,
        _7240,
        _7242,
        _7243,
        _7244,
        _7245,
        _7246,
        _7247,
        _7248,
        _7249,
        _7251,
        _7252,
        _7253,
        _7254,
        _7255,
        _7257,
        _7258,
        _7260,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7889,
        _7890,
        _7891,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6859,
        _6860,
        _6861,
        _6863,
        _6865,
        _6866,
        _6867,
        _6869,
        _6870,
        _6872,
        _6873,
        _6874,
        _6875,
        _6877,
        _6878,
        _6879,
        _6881,
        _6882,
        _6884,
        _6886,
        _6887,
        _6888,
        _6890,
        _6891,
        _6893,
        _6895,
        _6897,
        _6898,
        _6903,
        _6904,
        _6905,
        _6907,
        _6909,
        _6911,
        _6912,
        _6913,
        _6914,
        _6915,
        _6917,
        _6918,
        _6919,
        _6920,
        _6922,
        _6923,
        _6924,
        _6926,
        _6928,
        _6930,
        _6931,
        _6933,
        _6934,
        _6936,
        _6937,
        _6938,
        _6939,
        _6940,
        _6941,
        _6942,
        _6943,
        _6945,
        _6946,
        _6948,
        _6949,
        _6950,
        _6951,
        _6952,
        _6953,
        _6955,
        _6957,
        _6958,
        _6959,
        _6960,
        _6962,
        _6963,
        _6965,
        _6967,
        _6968,
        _6969,
        _6971,
        _6972,
        _6974,
        _6975,
        _6976,
        _6977,
        _6978,
        _6979,
        _6980,
        _6982,
        _6983,
        _6984,
        _6985,
        _6986,
        _6987,
        _6989,
        _6990,
        _6992,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6589,
        _6590,
        _6591,
        _6593,
        _6595,
        _6596,
        _6597,
        _6599,
        _6600,
        _6602,
        _6603,
        _6604,
        _6605,
        _6607,
        _6608,
        _6609,
        _6611,
        _6612,
        _6614,
        _6616,
        _6617,
        _6618,
        _6620,
        _6621,
        _6623,
        _6625,
        _6627,
        _6628,
        _6630,
        _6631,
        _6632,
        _6634,
        _6636,
        _6638,
        _6639,
        _6640,
        _6643,
        _6644,
        _6646,
        _6647,
        _6648,
        _6649,
        _6651,
        _6652,
        _6653,
        _6655,
        _6657,
        _6659,
        _6660,
        _6662,
        _6663,
        _6665,
        _6666,
        _6667,
        _6668,
        _6669,
        _6670,
        _6671,
        _6672,
        _6674,
        _6675,
        _6677,
        _6678,
        _6679,
        _6680,
        _6681,
        _6682,
        _6684,
        _6686,
        _6687,
        _6688,
        _6689,
        _6691,
        _6692,
        _6694,
        _6696,
        _6697,
        _6698,
        _6700,
        _6701,
        _6703,
        _6704,
        _6705,
        _6706,
        _6707,
        _6708,
        _6709,
        _6711,
        _6712,
        _6713,
        _6714,
        _6715,
        _6716,
        _6718,
        _6719,
        _6721,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5968,
        _5970,
        _5971,
        _5973,
        _5975,
        _5976,
        _5977,
        _5979,
        _5980,
        _5982,
        _5983,
        _5984,
        _5985,
        _5987,
        _5988,
        _5989,
        _5991,
        _5992,
        _5995,
        _5997,
        _5998,
        _5999,
        _6001,
        _6002,
        _6004,
        _6006,
        _6008,
        _6009,
        _6011,
        _6012,
        _6013,
        _6015,
        _6017,
        _6019,
        _6020,
        _6022,
        _6037,
        _6038,
        _6040,
        _6041,
        _6042,
        _6044,
        _6049,
        _6051,
        _6064,
        _6066,
        _6068,
        _6070,
        _6071,
        _6073,
        _6074,
        _6076,
        _6077,
        _6078,
        _6079,
        _6080,
        _6082,
        _6083,
        _6084,
        _6086,
        _6087,
        _6090,
        _6091,
        _6092,
        _6093,
        _6094,
        _6096,
        _6098,
        _6100,
        _6101,
        _6102,
        _6103,
        _6106,
        _6108,
        _6110,
        _6112,
        _6113,
        _6115,
        _6117,
        _6118,
        _6120,
        _6121,
        _6122,
        _6123,
        _6124,
        _6125,
        _6126,
        _6128,
        _6129,
        _6130,
        _6132,
        _6133,
        _6134,
        _6136,
        _6137,
        _6139,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6316,
        _6317,
        _6318,
        _6320,
        _6322,
        _6323,
        _6324,
        _6326,
        _6327,
        _6329,
        _6330,
        _6331,
        _6332,
        _6334,
        _6335,
        _6336,
        _6338,
        _6339,
        _6341,
        _6343,
        _6344,
        _6345,
        _6347,
        _6348,
        _6350,
        _6352,
        _6354,
        _6355,
        _6357,
        _6358,
        _6359,
        _6361,
        _6363,
        _6365,
        _6366,
        _6367,
        _6368,
        _6369,
        _6371,
        _6372,
        _6373,
        _6374,
        _6376,
        _6377,
        _6379,
        _6381,
        _6383,
        _6385,
        _6386,
        _6388,
        _6389,
        _6391,
        _6392,
        _6393,
        _6394,
        _6395,
        _6397,
        _6398,
        _6399,
        _6401,
        _6402,
        _6404,
        _6405,
        _6406,
        _6407,
        _6408,
        _6409,
        _6411,
        _6413,
        _6414,
        _6415,
        _6416,
        _6418,
        _6419,
        _6421,
        _6423,
        _6424,
        _6425,
        _6427,
        _6428,
        _6430,
        _6431,
        _6432,
        _6433,
        _6434,
        _6435,
        _6436,
        _6438,
        _6439,
        _6440,
        _6441,
        _6442,
        _6443,
        _6445,
        _6446,
        _6448,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5659,
        _5660,
        _5661,
        _5664,
        _5665,
        _5667,
        _5669,
        _5672,
        _5674,
        _5675,
        _5676,
        _5677,
        _5679,
        _5680,
        _5681,
        _5682,
        _5684,
        _5685,
        _5688,
        _5690,
        _5691,
        _5693,
        _5694,
        _5696,
        _5697,
        _5699,
        _5701,
        _5702,
        _5704,
        _5705,
        _5706,
        _5708,
        _5711,
        _5712,
        _5713,
        _5714,
        _5715,
        _5717,
        _5718,
        _5719,
        _5720,
        _5723,
        _5724,
        _5725,
        _5727,
        _5728,
        _5735,
        _5736,
        _5738,
        _5739,
        _5741,
        _5742,
        _5743,
        _5747,
        _5748,
        _5749,
        _5750,
        _5752,
        _5753,
        _5755,
        _5756,
        _5758,
        _5759,
        _5760,
        _5761,
        _5762,
        _5763,
        _5765,
        _5767,
        _5768,
        _5771,
        _5772,
        _5775,
        _5777,
        _5778,
        _5781,
        _5782,
        _5784,
        _5785,
        _5787,
        _5788,
        _5789,
        _5790,
        _5791,
        _5792,
        _5793,
        _5794,
        _5797,
        _5798,
        _5800,
        _5801,
        _5802,
        _5805,
        _5806,
        _5808,
        _5809,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4842,
        _4843,
        _4844,
        _4847,
        _4848,
        _4849,
        _4850,
        _4852,
        _4854,
        _4855,
        _4856,
        _4857,
        _4859,
        _4860,
        _4861,
        _4862,
        _4864,
        _4865,
        _4867,
        _4869,
        _4870,
        _4872,
        _4873,
        _4875,
        _4876,
        _4878,
        _4881,
        _4882,
        _4884,
        _4885,
        _4886,
        _4888,
        _4891,
        _4892,
        _4893,
        _4894,
        _4898,
        _4900,
        _4901,
        _4902,
        _4903,
        _4906,
        _4907,
        _4908,
        _4910,
        _4911,
        _4914,
        _4915,
        _4917,
        _4918,
        _4920,
        _4921,
        _4922,
        _4923,
        _4924,
        _4925,
        _4931,
        _4933,
        _4935,
        _4937,
        _4938,
        _4940,
        _4941,
        _4942,
        _4943,
        _4944,
        _4945,
        _4947,
        _4949,
        _4950,
        _4951,
        _4952,
        _4955,
        _4957,
        _4958,
        _4960,
        _4961,
        _4963,
        _4964,
        _4966,
        _4967,
        _4968,
        _4969,
        _4970,
        _4971,
        _4972,
        _4973,
        _4975,
        _4976,
        _4977,
        _4978,
        _4979,
        _4984,
        _4985,
        _4987,
        _4988,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5396,
        _5397,
        _5398,
        _5401,
        _5402,
        _5403,
        _5404,
        _5406,
        _5408,
        _5409,
        _5410,
        _5411,
        _5413,
        _5414,
        _5415,
        _5416,
        _5418,
        _5419,
        _5421,
        _5423,
        _5424,
        _5426,
        _5427,
        _5429,
        _5430,
        _5432,
        _5434,
        _5435,
        _5437,
        _5438,
        _5439,
        _5441,
        _5444,
        _5445,
        _5446,
        _5447,
        _5448,
        _5450,
        _5451,
        _5452,
        _5453,
        _5455,
        _5456,
        _5457,
        _5459,
        _5460,
        _5463,
        _5464,
        _5466,
        _5467,
        _5469,
        _5470,
        _5471,
        _5472,
        _5473,
        _5474,
        _5476,
        _5477,
        _5478,
        _5480,
        _5481,
        _5483,
        _5484,
        _5485,
        _5486,
        _5487,
        _5488,
        _5490,
        _5492,
        _5493,
        _5494,
        _5495,
        _5497,
        _5499,
        _5500,
        _5502,
        _5503,
        _5505,
        _5506,
        _5508,
        _5509,
        _5510,
        _5511,
        _5512,
        _5513,
        _5514,
        _5515,
        _5517,
        _5518,
        _5519,
        _5520,
        _5521,
        _5523,
        _5524,
        _5526,
        _5527,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5132,
        _5133,
        _5134,
        _5137,
        _5138,
        _5139,
        _5140,
        _5142,
        _5144,
        _5145,
        _5146,
        _5147,
        _5149,
        _5150,
        _5151,
        _5152,
        _5154,
        _5155,
        _5157,
        _5159,
        _5160,
        _5162,
        _5163,
        _5165,
        _5166,
        _5168,
        _5170,
        _5171,
        _5173,
        _5174,
        _5175,
        _5177,
        _5180,
        _5181,
        _5182,
        _5183,
        _5185,
        _5187,
        _5188,
        _5189,
        _5190,
        _5192,
        _5193,
        _5194,
        _5196,
        _5197,
        _5200,
        _5201,
        _5203,
        _5204,
        _5206,
        _5207,
        _5208,
        _5209,
        _5210,
        _5211,
        _5213,
        _5214,
        _5215,
        _5217,
        _5218,
        _5220,
        _5221,
        _5222,
        _5223,
        _5224,
        _5225,
        _5227,
        _5229,
        _5230,
        _5231,
        _5232,
        _5234,
        _5236,
        _5237,
        _5239,
        _5240,
        _5242,
        _5243,
        _5245,
        _5246,
        _5247,
        _5248,
        _5249,
        _5250,
        _5251,
        _5252,
        _5254,
        _5255,
        _5256,
        _5257,
        _5258,
        _5260,
        _5261,
        _5263,
        _5264,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4561,
        _4562,
        _4563,
        _4566,
        _4567,
        _4568,
        _4569,
        _4571,
        _4573,
        _4574,
        _4575,
        _4576,
        _4578,
        _4579,
        _4580,
        _4581,
        _4583,
        _4584,
        _4586,
        _4588,
        _4589,
        _4591,
        _4592,
        _4594,
        _4595,
        _4597,
        _4599,
        _4600,
        _4602,
        _4603,
        _4604,
        _4606,
        _4609,
        _4610,
        _4611,
        _4612,
        _4620,
        _4622,
        _4623,
        _4624,
        _4625,
        _4627,
        _4628,
        _4629,
        _4631,
        _4632,
        _4635,
        _4636,
        _4638,
        _4639,
        _4641,
        _4642,
        _4643,
        _4644,
        _4645,
        _4646,
        _4648,
        _4649,
        _4661,
        _4663,
        _4664,
        _4666,
        _4667,
        _4668,
        _4669,
        _4670,
        _4671,
        _4673,
        _4675,
        _4676,
        _4677,
        _4678,
        _4680,
        _4682,
        _4683,
        _4685,
        _4686,
        _4688,
        _4689,
        _4691,
        _4692,
        _4693,
        _4694,
        _4695,
        _4696,
        _4697,
        _4698,
        _4700,
        _4701,
        _4702,
        _4703,
        _4704,
        _4706,
        _4707,
        _4709,
        _4710,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4293,
        _4294,
        _4295,
        _4298,
        _4299,
        _4300,
        _4301,
        _4303,
        _4305,
        _4306,
        _4307,
        _4308,
        _4310,
        _4311,
        _4312,
        _4313,
        _4315,
        _4316,
        _4318,
        _4320,
        _4321,
        _4323,
        _4324,
        _4326,
        _4327,
        _4329,
        _4331,
        _4332,
        _4334,
        _4335,
        _4336,
        _4339,
        _4342,
        _4343,
        _4344,
        _4345,
        _4346,
        _4348,
        _4349,
        _4352,
        _4353,
        _4355,
        _4356,
        _4357,
        _4359,
        _4360,
        _4363,
        _4364,
        _4366,
        _4367,
        _4369,
        _4370,
        _4371,
        _4372,
        _4373,
        _4374,
        _4375,
        _4376,
        _4377,
        _4379,
        _4380,
        _4382,
        _4383,
        _4384,
        _4387,
        _4388,
        _4389,
        _4391,
        _4393,
        _4394,
        _4395,
        _4396,
        _4398,
        _4400,
        _4401,
        _4403,
        _4404,
        _4406,
        _4407,
        _4409,
        _4410,
        _4411,
        _4412,
        _4413,
        _4414,
        _4415,
        _4416,
        _4419,
        _4420,
        _4421,
        _4422,
        _4423,
        _4425,
        _4426,
        _4428,
        _4429,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4020,
        _4021,
        _4022,
        _4025,
        _4026,
        _4027,
        _4028,
        _4030,
        _4032,
        _4033,
        _4034,
        _4035,
        _4037,
        _4038,
        _4039,
        _4040,
        _4042,
        _4043,
        _4045,
        _4047,
        _4048,
        _4050,
        _4051,
        _4053,
        _4054,
        _4056,
        _4058,
        _4059,
        _4062,
        _4063,
        _4064,
        _4067,
        _4069,
        _4070,
        _4071,
        _4072,
        _4074,
        _4076,
        _4077,
        _4078,
        _4079,
        _4081,
        _4082,
        _4083,
        _4085,
        _4086,
        _4089,
        _4090,
        _4092,
        _4093,
        _4095,
        _4096,
        _4097,
        _4098,
        _4099,
        _4100,
        _4101,
        _4102,
        _4103,
        _4105,
        _4106,
        _4108,
        _4109,
        _4110,
        _4111,
        _4112,
        _4113,
        _4115,
        _4117,
        _4118,
        _4119,
        _4120,
        _4122,
        _4124,
        _4125,
        _4127,
        _4128,
        _4133,
        _4134,
        _4136,
        _4137,
        _4138,
        _4139,
        _4140,
        _4141,
        _4142,
        _4143,
        _4145,
        _4146,
        _4147,
        _4148,
        _4149,
        _4151,
        _4152,
        _4154,
        _4155,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7675,
        _7676,
        _7677,
        _7682,
        _7684,
        _7687,
        _7688,
        _7690,
        _7691,
        _7693,
        _7694,
        _7695,
        _7696,
        _7698,
        _7699,
        _7700,
        _7702,
        _7703,
        _7706,
        _7708,
        _7709,
        _7710,
        _7712,
        _7713,
        _7717,
        _7719,
        _7721,
        _7722,
        _7724,
        _7725,
        _7726,
        _7728,
        _7730,
        _7734,
        _7735,
        _7738,
        _7752,
        _7753,
        _7755,
        _7756,
        _7757,
        _7759,
        _7764,
        _7765,
        _7774,
        _7776,
        _7781,
        _7783,
        _7784,
        _7786,
        _7787,
        _7789,
        _7790,
        _7791,
        _7793,
        _7794,
        _7795,
        _7797,
        _7799,
        _7801,
        _7802,
        _7804,
        _7806,
        _7809,
        _7810,
        _7811,
        _7814,
        _7816,
        _7818,
        _7819,
        _7820,
        _7821,
        _7823,
        _7824,
        _7826,
        _7828,
        _7829,
        _7830,
        _7832,
        _7833,
        _7835,
        _7836,
        _7837,
        _7838,
        _7839,
        _7840,
        _7841,
        _7845,
        _7846,
        _7847,
        _7852,
        _7853,
        _7854,
        _7856,
        _7857,
        _7859,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3228,
        _3229,
        _3230,
        _3233,
        _3234,
        _3235,
        _3236,
        _3238,
        _3240,
        _3241,
        _3242,
        _3243,
        _3245,
        _3246,
        _3247,
        _3248,
        _3250,
        _3251,
        _3253,
        _3255,
        _3256,
        _3258,
        _3259,
        _3261,
        _3262,
        _3264,
        _3266,
        _3267,
        _3269,
        _3270,
        _3271,
        _3274,
        _3276,
        _3277,
        _3278,
        _3279,
        _3281,
        _3283,
        _3284,
        _3285,
        _3286,
        _3288,
        _3289,
        _3290,
        _3292,
        _3293,
        _3296,
        _3297,
        _3299,
        _3300,
        _3302,
        _3303,
        _3304,
        _3305,
        _3306,
        _3307,
        _3308,
        _3309,
        _3310,
        _3312,
        _3313,
        _3315,
        _3316,
        _3317,
        _3318,
        _3319,
        _3320,
        _3322,
        _3324,
        _3325,
        _3326,
        _3327,
        _3329,
        _3331,
        _3332,
        _3334,
        _3335,
        _3340,
        _3341,
        _3343,
        _3344,
        _3345,
        _3346,
        _3347,
        _3348,
        _3349,
        _3350,
        _3352,
        _3353,
        _3354,
        _3355,
        _3356,
        _3358,
        _3359,
        _3361,
        _3362,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3757,
        _3758,
        _3759,
        _3762,
        _3763,
        _3764,
        _3765,
        _3767,
        _3769,
        _3770,
        _3771,
        _3772,
        _3774,
        _3775,
        _3776,
        _3777,
        _3779,
        _3780,
        _3782,
        _3784,
        _3785,
        _3787,
        _3788,
        _3790,
        _3791,
        _3793,
        _3795,
        _3796,
        _3798,
        _3799,
        _3800,
        _3803,
        _3805,
        _3806,
        _3807,
        _3808,
        _3809,
        _3811,
        _3812,
        _3813,
        _3814,
        _3816,
        _3817,
        _3818,
        _3820,
        _3821,
        _3824,
        _3825,
        _3827,
        _3828,
        _3830,
        _3831,
        _3832,
        _3833,
        _3834,
        _3835,
        _3836,
        _3837,
        _3838,
        _3840,
        _3841,
        _3843,
        _3844,
        _3845,
        _3846,
        _3847,
        _3848,
        _3850,
        _3852,
        _3853,
        _3854,
        _3855,
        _3857,
        _3859,
        _3860,
        _3862,
        _3863,
        _3866,
        _3867,
        _3869,
        _3870,
        _3871,
        _3872,
        _3873,
        _3874,
        _3875,
        _3876,
        _3878,
        _3879,
        _3880,
        _3881,
        _3882,
        _3884,
        _3885,
        _3887,
        _3888,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3494,
        _3495,
        _3496,
        _3499,
        _3500,
        _3501,
        _3502,
        _3504,
        _3506,
        _3507,
        _3508,
        _3509,
        _3511,
        _3512,
        _3513,
        _3514,
        _3516,
        _3517,
        _3519,
        _3521,
        _3522,
        _3524,
        _3525,
        _3527,
        _3528,
        _3530,
        _3532,
        _3533,
        _3535,
        _3536,
        _3537,
        _3540,
        _3542,
        _3543,
        _3544,
        _3545,
        _3546,
        _3548,
        _3549,
        _3550,
        _3551,
        _3553,
        _3554,
        _3555,
        _3557,
        _3558,
        _3561,
        _3562,
        _3564,
        _3565,
        _3567,
        _3568,
        _3569,
        _3570,
        _3571,
        _3572,
        _3573,
        _3574,
        _3575,
        _3577,
        _3578,
        _3580,
        _3581,
        _3582,
        _3583,
        _3584,
        _3585,
        _3587,
        _3589,
        _3590,
        _3591,
        _3592,
        _3594,
        _3596,
        _3597,
        _3599,
        _3600,
        _3603,
        _3604,
        _3606,
        _3607,
        _3608,
        _3609,
        _3610,
        _3611,
        _3612,
        _3613,
        _3615,
        _3616,
        _3617,
        _3618,
        _3619,
        _3621,
        _3622,
        _3624,
        _3625,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2926,
        _2927,
        _2928,
        _2931,
        _2932,
        _2933,
        _2939,
        _2941,
        _2943,
        _2944,
        _2945,
        _2946,
        _2948,
        _2949,
        _2950,
        _2951,
        _2953,
        _2954,
        _2956,
        _2959,
        _2960,
        _2962,
        _2963,
        _2966,
        _2967,
        _2969,
        _2971,
        _2972,
        _2974,
        _2975,
        _2976,
        _2979,
        _2983,
        _2984,
        _2985,
        _2986,
        _2987,
        _2988,
        _2991,
        _2992,
        _2993,
        _2996,
        _2997,
        _2998,
        _2999,
        _3001,
        _3002,
        _3003,
        _3005,
        _3006,
        _3010,
        _3011,
        _3013,
        _3014,
        _3016,
        _3017,
        _3020,
        _3021,
        _3023,
        _3024,
        _3025,
        _3027,
        _3028,
        _3030,
        _3031,
        _3033,
        _3034,
        _3035,
        _3036,
        _3037,
        _3040,
        _3042,
        _3043,
        _3044,
        _3047,
        _3049,
        _3051,
        _3052,
        _3054,
        _3055,
        _3057,
        _3058,
        _3060,
        _3061,
        _3062,
        _3063,
        _3064,
        _3065,
        _3066,
        _3067,
        _3072,
        _3073,
        _3074,
        _3077,
        _3078,
        _3080,
        _3081,
        _3083,
        _3084,
    )

    Self = TypeVar("Self", bound="PartAnalysis")
    CastSelf = TypeVar("CastSelf", bound="PartAnalysis._Cast_PartAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("PartAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartAnalysis:
    """Special nested class for casting PartAnalysis to subclasses."""

    __parent__: "PartAnalysis"

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2926.AbstractAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2926,
        )

        return self.__parent__._cast(_2926.AbstractAssemblySystemDeflection)

    @property
    def abstract_shaft_or_housing_system_deflection(
        self: "CastSelf",
    ) -> "_2927.AbstractShaftOrHousingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2927,
        )

        return self.__parent__._cast(_2927.AbstractShaftOrHousingSystemDeflection)

    @property
    def abstract_shaft_system_deflection(
        self: "CastSelf",
    ) -> "_2928.AbstractShaftSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2928,
        )

        return self.__parent__._cast(_2928.AbstractShaftSystemDeflection)

    @property
    def agma_gleason_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2931.AGMAGleasonConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2931,
        )

        return self.__parent__._cast(_2931.AGMAGleasonConicalGearSetSystemDeflection)

    @property
    def agma_gleason_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2932.AGMAGleasonConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2932,
        )

        return self.__parent__._cast(_2932.AGMAGleasonConicalGearSystemDeflection)

    @property
    def assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2933.AssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2933,
        )

        return self.__parent__._cast(_2933.AssemblySystemDeflection)

    @property
    def bearing_system_deflection(self: "CastSelf") -> "_2939.BearingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2939,
        )

        return self.__parent__._cast(_2939.BearingSystemDeflection)

    @property
    def belt_drive_system_deflection(
        self: "CastSelf",
    ) -> "_2941.BeltDriveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2941,
        )

        return self.__parent__._cast(_2941.BeltDriveSystemDeflection)

    @property
    def bevel_differential_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2943.BevelDifferentialGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2943,
        )

        return self.__parent__._cast(_2943.BevelDifferentialGearSetSystemDeflection)

    @property
    def bevel_differential_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2944.BevelDifferentialGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2944,
        )

        return self.__parent__._cast(_2944.BevelDifferentialGearSystemDeflection)

    @property
    def bevel_differential_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2945.BevelDifferentialPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2945,
        )

        return self.__parent__._cast(_2945.BevelDifferentialPlanetGearSystemDeflection)

    @property
    def bevel_differential_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2946.BevelDifferentialSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2946,
        )

        return self.__parent__._cast(_2946.BevelDifferentialSunGearSystemDeflection)

    @property
    def bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2948.BevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2948,
        )

        return self.__parent__._cast(_2948.BevelGearSetSystemDeflection)

    @property
    def bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2949.BevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2949,
        )

        return self.__parent__._cast(_2949.BevelGearSystemDeflection)

    @property
    def bolted_joint_system_deflection(
        self: "CastSelf",
    ) -> "_2950.BoltedJointSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2950,
        )

        return self.__parent__._cast(_2950.BoltedJointSystemDeflection)

    @property
    def bolt_system_deflection(self: "CastSelf") -> "_2951.BoltSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2951,
        )

        return self.__parent__._cast(_2951.BoltSystemDeflection)

    @property
    def clutch_half_system_deflection(
        self: "CastSelf",
    ) -> "_2953.ClutchHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2953,
        )

        return self.__parent__._cast(_2953.ClutchHalfSystemDeflection)

    @property
    def clutch_system_deflection(self: "CastSelf") -> "_2954.ClutchSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2954,
        )

        return self.__parent__._cast(_2954.ClutchSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2956.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2956,
        )

        return self.__parent__._cast(_2956.ComponentSystemDeflection)

    @property
    def concept_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2959.ConceptCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2959,
        )

        return self.__parent__._cast(_2959.ConceptCouplingHalfSystemDeflection)

    @property
    def concept_coupling_system_deflection(
        self: "CastSelf",
    ) -> "_2960.ConceptCouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2960,
        )

        return self.__parent__._cast(_2960.ConceptCouplingSystemDeflection)

    @property
    def concept_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2962.ConceptGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2962,
        )

        return self.__parent__._cast(_2962.ConceptGearSetSystemDeflection)

    @property
    def concept_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2963.ConceptGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2963,
        )

        return self.__parent__._cast(_2963.ConceptGearSystemDeflection)

    @property
    def conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2966.ConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2966,
        )

        return self.__parent__._cast(_2966.ConicalGearSetSystemDeflection)

    @property
    def conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2967.ConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2967,
        )

        return self.__parent__._cast(_2967.ConicalGearSystemDeflection)

    @property
    def connector_system_deflection(
        self: "CastSelf",
    ) -> "_2969.ConnectorSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2969,
        )

        return self.__parent__._cast(_2969.ConnectorSystemDeflection)

    @property
    def coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2971.CouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2971,
        )

        return self.__parent__._cast(_2971.CouplingHalfSystemDeflection)

    @property
    def coupling_system_deflection(
        self: "CastSelf",
    ) -> "_2972.CouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2972,
        )

        return self.__parent__._cast(_2972.CouplingSystemDeflection)

    @property
    def cvt_pulley_system_deflection(
        self: "CastSelf",
    ) -> "_2974.CVTPulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2974,
        )

        return self.__parent__._cast(_2974.CVTPulleySystemDeflection)

    @property
    def cvt_system_deflection(self: "CastSelf") -> "_2975.CVTSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2975,
        )

        return self.__parent__._cast(_2975.CVTSystemDeflection)

    @property
    def cycloidal_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2976.CycloidalAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2976,
        )

        return self.__parent__._cast(_2976.CycloidalAssemblySystemDeflection)

    @property
    def cycloidal_disc_system_deflection(
        self: "CastSelf",
    ) -> "_2979.CycloidalDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2979,
        )

        return self.__parent__._cast(_2979.CycloidalDiscSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2983.CylindricalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2983,
        )

        return self.__parent__._cast(_2983.CylindricalGearSetSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2984.CylindricalGearSetSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2984,
        )

        return self.__parent__._cast(_2984.CylindricalGearSetSystemDeflectionTimestep)

    @property
    def cylindrical_gear_set_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2985.CylindricalGearSetSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2985,
        )

        return self.__parent__._cast(
            _2985.CylindricalGearSetSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2986.CylindricalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2986,
        )

        return self.__parent__._cast(_2986.CylindricalGearSystemDeflection)

    @property
    def cylindrical_gear_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2987.CylindricalGearSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2987,
        )

        return self.__parent__._cast(_2987.CylindricalGearSystemDeflectionTimestep)

    @property
    def cylindrical_gear_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2988.CylindricalGearSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2988,
        )

        return self.__parent__._cast(
            _2988.CylindricalGearSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2991.CylindricalPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2991,
        )

        return self.__parent__._cast(_2991.CylindricalPlanetGearSystemDeflection)

    @property
    def datum_system_deflection(self: "CastSelf") -> "_2992.DatumSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2992,
        )

        return self.__parent__._cast(_2992.DatumSystemDeflection)

    @property
    def external_cad_model_system_deflection(
        self: "CastSelf",
    ) -> "_2993.ExternalCADModelSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2993,
        )

        return self.__parent__._cast(_2993.ExternalCADModelSystemDeflection)

    @property
    def face_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2996.FaceGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2996,
        )

        return self.__parent__._cast(_2996.FaceGearSetSystemDeflection)

    @property
    def face_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2997.FaceGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2997,
        )

        return self.__parent__._cast(_2997.FaceGearSystemDeflection)

    @property
    def fe_part_system_deflection(self: "CastSelf") -> "_2998.FEPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2998,
        )

        return self.__parent__._cast(_2998.FEPartSystemDeflection)

    @property
    def flexible_pin_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2999.FlexiblePinAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2999,
        )

        return self.__parent__._cast(_2999.FlexiblePinAssemblySystemDeflection)

    @property
    def gear_set_system_deflection(self: "CastSelf") -> "_3001.GearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3001,
        )

        return self.__parent__._cast(_3001.GearSetSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "_3002.GearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3002,
        )

        return self.__parent__._cast(_3002.GearSystemDeflection)

    @property
    def guide_dxf_model_system_deflection(
        self: "CastSelf",
    ) -> "_3003.GuideDxfModelSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3003,
        )

        return self.__parent__._cast(_3003.GuideDxfModelSystemDeflection)

    @property
    def hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3005.HypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3005,
        )

        return self.__parent__._cast(_3005.HypoidGearSetSystemDeflection)

    @property
    def hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3006.HypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3006,
        )

        return self.__parent__._cast(_3006.HypoidGearSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3010.KlingelnbergCycloPalloidConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3010,
        )

        return self.__parent__._cast(
            _3010.KlingelnbergCycloPalloidConicalGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3011.KlingelnbergCycloPalloidConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3011,
        )

        return self.__parent__._cast(
            _3011.KlingelnbergCycloPalloidConicalGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3013.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3013,
        )

        return self.__parent__._cast(
            _3013.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3014,
        )

        return self.__parent__._cast(
            _3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3016.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3016,
        )

        return self.__parent__._cast(
            _3016.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3017.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3017,
        )

        return self.__parent__._cast(
            _3017.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
        )

    @property
    def mass_disc_system_deflection(
        self: "CastSelf",
    ) -> "_3020.MassDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3020,
        )

        return self.__parent__._cast(_3020.MassDiscSystemDeflection)

    @property
    def measurement_component_system_deflection(
        self: "CastSelf",
    ) -> "_3021.MeasurementComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3021,
        )

        return self.__parent__._cast(_3021.MeasurementComponentSystemDeflection)

    @property
    def microphone_array_system_deflection(
        self: "CastSelf",
    ) -> "_3023.MicrophoneArraySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3023,
        )

        return self.__parent__._cast(_3023.MicrophoneArraySystemDeflection)

    @property
    def microphone_system_deflection(
        self: "CastSelf",
    ) -> "_3024.MicrophoneSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3024,
        )

        return self.__parent__._cast(_3024.MicrophoneSystemDeflection)

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_3025.MountableComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3025,
        )

        return self.__parent__._cast(_3025.MountableComponentSystemDeflection)

    @property
    def oil_seal_system_deflection(self: "CastSelf") -> "_3027.OilSealSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3027,
        )

        return self.__parent__._cast(_3027.OilSealSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_3028.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3028,
        )

        return self.__parent__._cast(_3028.PartSystemDeflection)

    @property
    def part_to_part_shear_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_3030.PartToPartShearCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3030,
        )

        return self.__parent__._cast(_3030.PartToPartShearCouplingHalfSystemDeflection)

    @property
    def part_to_part_shear_coupling_system_deflection(
        self: "CastSelf",
    ) -> "_3031.PartToPartShearCouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3031,
        )

        return self.__parent__._cast(_3031.PartToPartShearCouplingSystemDeflection)

    @property
    def planet_carrier_system_deflection(
        self: "CastSelf",
    ) -> "_3033.PlanetCarrierSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3033,
        )

        return self.__parent__._cast(_3033.PlanetCarrierSystemDeflection)

    @property
    def point_load_system_deflection(
        self: "CastSelf",
    ) -> "_3034.PointLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3034,
        )

        return self.__parent__._cast(_3034.PointLoadSystemDeflection)

    @property
    def power_load_system_deflection(
        self: "CastSelf",
    ) -> "_3035.PowerLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3035,
        )

        return self.__parent__._cast(_3035.PowerLoadSystemDeflection)

    @property
    def pulley_system_deflection(self: "CastSelf") -> "_3036.PulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3036,
        )

        return self.__parent__._cast(_3036.PulleySystemDeflection)

    @property
    def ring_pins_system_deflection(
        self: "CastSelf",
    ) -> "_3037.RingPinsSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3037,
        )

        return self.__parent__._cast(_3037.RingPinsSystemDeflection)

    @property
    def rolling_ring_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_3040.RollingRingAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3040,
        )

        return self.__parent__._cast(_3040.RollingRingAssemblySystemDeflection)

    @property
    def rolling_ring_system_deflection(
        self: "CastSelf",
    ) -> "_3042.RollingRingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3042,
        )

        return self.__parent__._cast(_3042.RollingRingSystemDeflection)

    @property
    def root_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_3043.RootAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3043,
        )

        return self.__parent__._cast(_3043.RootAssemblySystemDeflection)

    @property
    def shaft_hub_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3044.ShaftHubConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3044,
        )

        return self.__parent__._cast(_3044.ShaftHubConnectionSystemDeflection)

    @property
    def shaft_system_deflection(self: "CastSelf") -> "_3047.ShaftSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3047,
        )

        return self.__parent__._cast(_3047.ShaftSystemDeflection)

    @property
    def specialised_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_3049.SpecialisedAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3049,
        )

        return self.__parent__._cast(_3049.SpecialisedAssemblySystemDeflection)

    @property
    def spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3051.SpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3051,
        )

        return self.__parent__._cast(_3051.SpiralBevelGearSetSystemDeflection)

    @property
    def spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3052.SpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3052,
        )

        return self.__parent__._cast(_3052.SpiralBevelGearSystemDeflection)

    @property
    def spring_damper_half_system_deflection(
        self: "CastSelf",
    ) -> "_3054.SpringDamperHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3054,
        )

        return self.__parent__._cast(_3054.SpringDamperHalfSystemDeflection)

    @property
    def spring_damper_system_deflection(
        self: "CastSelf",
    ) -> "_3055.SpringDamperSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3055,
        )

        return self.__parent__._cast(_3055.SpringDamperSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3057.StraightBevelDiffGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3057,
        )

        return self.__parent__._cast(_3057.StraightBevelDiffGearSetSystemDeflection)

    @property
    def straight_bevel_diff_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3058.StraightBevelDiffGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3058,
        )

        return self.__parent__._cast(_3058.StraightBevelDiffGearSystemDeflection)

    @property
    def straight_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3060.StraightBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3060,
        )

        return self.__parent__._cast(_3060.StraightBevelGearSetSystemDeflection)

    @property
    def straight_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3061.StraightBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3061,
        )

        return self.__parent__._cast(_3061.StraightBevelGearSystemDeflection)

    @property
    def straight_bevel_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3062.StraightBevelPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3062,
        )

        return self.__parent__._cast(_3062.StraightBevelPlanetGearSystemDeflection)

    @property
    def straight_bevel_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3063.StraightBevelSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3063,
        )

        return self.__parent__._cast(_3063.StraightBevelSunGearSystemDeflection)

    @property
    def synchroniser_half_system_deflection(
        self: "CastSelf",
    ) -> "_3064.SynchroniserHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3064,
        )

        return self.__parent__._cast(_3064.SynchroniserHalfSystemDeflection)

    @property
    def synchroniser_part_system_deflection(
        self: "CastSelf",
    ) -> "_3065.SynchroniserPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3065,
        )

        return self.__parent__._cast(_3065.SynchroniserPartSystemDeflection)

    @property
    def synchroniser_sleeve_system_deflection(
        self: "CastSelf",
    ) -> "_3066.SynchroniserSleeveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3066,
        )

        return self.__parent__._cast(_3066.SynchroniserSleeveSystemDeflection)

    @property
    def synchroniser_system_deflection(
        self: "CastSelf",
    ) -> "_3067.SynchroniserSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3067,
        )

        return self.__parent__._cast(_3067.SynchroniserSystemDeflection)

    @property
    def torque_converter_pump_system_deflection(
        self: "CastSelf",
    ) -> "_3072.TorqueConverterPumpSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3072,
        )

        return self.__parent__._cast(_3072.TorqueConverterPumpSystemDeflection)

    @property
    def torque_converter_system_deflection(
        self: "CastSelf",
    ) -> "_3073.TorqueConverterSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3073,
        )

        return self.__parent__._cast(_3073.TorqueConverterSystemDeflection)

    @property
    def torque_converter_turbine_system_deflection(
        self: "CastSelf",
    ) -> "_3074.TorqueConverterTurbineSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3074,
        )

        return self.__parent__._cast(_3074.TorqueConverterTurbineSystemDeflection)

    @property
    def unbalanced_mass_system_deflection(
        self: "CastSelf",
    ) -> "_3077.UnbalancedMassSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3077,
        )

        return self.__parent__._cast(_3077.UnbalancedMassSystemDeflection)

    @property
    def virtual_component_system_deflection(
        self: "CastSelf",
    ) -> "_3078.VirtualComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3078,
        )

        return self.__parent__._cast(_3078.VirtualComponentSystemDeflection)

    @property
    def worm_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3080.WormGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3080,
        )

        return self.__parent__._cast(_3080.WormGearSetSystemDeflection)

    @property
    def worm_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3081.WormGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3081,
        )

        return self.__parent__._cast(_3081.WormGearSystemDeflection)

    @property
    def zerol_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3083.ZerolBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3083,
        )

        return self.__parent__._cast(_3083.ZerolBevelGearSetSystemDeflection)

    @property
    def zerol_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3084.ZerolBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3084,
        )

        return self.__parent__._cast(_3084.ZerolBevelGearSystemDeflection)

    @property
    def abstract_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3228.AbstractAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3228,
        )

        return self.__parent__._cast(
            _3228.AbstractAssemblySteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_or_housing_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3229.AbstractShaftOrHousingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3229,
        )

        return self.__parent__._cast(
            _3229.AbstractShaftOrHousingSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3230.AbstractShaftSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3230,
        )

        return self.__parent__._cast(_3230.AbstractShaftSteadyStateSynchronousResponse)

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3233.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3233,
        )

        return self.__parent__._cast(
            _3233.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse
        )

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3234.AGMAGleasonConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3234,
        )

        return self.__parent__._cast(
            _3234.AGMAGleasonConicalGearSteadyStateSynchronousResponse
        )

    @property
    def assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3235.AssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3235,
        )

        return self.__parent__._cast(_3235.AssemblySteadyStateSynchronousResponse)

    @property
    def bearing_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3236.BearingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3236,
        )

        return self.__parent__._cast(_3236.BearingSteadyStateSynchronousResponse)

    @property
    def belt_drive_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3238.BeltDriveSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3238,
        )

        return self.__parent__._cast(_3238.BeltDriveSteadyStateSynchronousResponse)

    @property
    def bevel_differential_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3240.BevelDifferentialGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3240,
        )

        return self.__parent__._cast(
            _3240.BevelDifferentialGearSetSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3241.BevelDifferentialGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3241,
        )

        return self.__parent__._cast(
            _3241.BevelDifferentialGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3242.BevelDifferentialPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3242,
        )

        return self.__parent__._cast(
            _3242.BevelDifferentialPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3243.BevelDifferentialSunGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3243,
        )

        return self.__parent__._cast(
            _3243.BevelDifferentialSunGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3245.BevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3245,
        )

        return self.__parent__._cast(_3245.BevelGearSetSteadyStateSynchronousResponse)

    @property
    def bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3246.BevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3246,
        )

        return self.__parent__._cast(_3246.BevelGearSteadyStateSynchronousResponse)

    @property
    def bolted_joint_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3247.BoltedJointSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3247,
        )

        return self.__parent__._cast(_3247.BoltedJointSteadyStateSynchronousResponse)

    @property
    def bolt_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3248.BoltSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3248,
        )

        return self.__parent__._cast(_3248.BoltSteadyStateSynchronousResponse)

    @property
    def clutch_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3250.ClutchHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3250,
        )

        return self.__parent__._cast(_3250.ClutchHalfSteadyStateSynchronousResponse)

    @property
    def clutch_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3251.ClutchSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3251,
        )

        return self.__parent__._cast(_3251.ClutchSteadyStateSynchronousResponse)

    @property
    def component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3253.ComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3253,
        )

        return self.__parent__._cast(_3253.ComponentSteadyStateSynchronousResponse)

    @property
    def concept_coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3255.ConceptCouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3255,
        )

        return self.__parent__._cast(
            _3255.ConceptCouplingHalfSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3256.ConceptCouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3256,
        )

        return self.__parent__._cast(
            _3256.ConceptCouplingSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3258.ConceptGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3258,
        )

        return self.__parent__._cast(_3258.ConceptGearSetSteadyStateSynchronousResponse)

    @property
    def concept_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3259.ConceptGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3259,
        )

        return self.__parent__._cast(_3259.ConceptGearSteadyStateSynchronousResponse)

    @property
    def conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3261.ConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3261,
        )

        return self.__parent__._cast(_3261.ConicalGearSetSteadyStateSynchronousResponse)

    @property
    def conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3262.ConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3262,
        )

        return self.__parent__._cast(_3262.ConicalGearSteadyStateSynchronousResponse)

    @property
    def connector_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3264.ConnectorSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3264,
        )

        return self.__parent__._cast(_3264.ConnectorSteadyStateSynchronousResponse)

    @property
    def coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3266.CouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3266,
        )

        return self.__parent__._cast(_3266.CouplingHalfSteadyStateSynchronousResponse)

    @property
    def coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3267.CouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3267,
        )

        return self.__parent__._cast(_3267.CouplingSteadyStateSynchronousResponse)

    @property
    def cvt_pulley_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3269.CVTPulleySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3269,
        )

        return self.__parent__._cast(_3269.CVTPulleySteadyStateSynchronousResponse)

    @property
    def cvt_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3270.CVTSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3270,
        )

        return self.__parent__._cast(_3270.CVTSteadyStateSynchronousResponse)

    @property
    def cycloidal_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3271.CycloidalAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3271,
        )

        return self.__parent__._cast(
            _3271.CycloidalAssemblySteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3274.CycloidalDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3274,
        )

        return self.__parent__._cast(_3274.CycloidalDiscSteadyStateSynchronousResponse)

    @property
    def cylindrical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3276.CylindricalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3276,
        )

        return self.__parent__._cast(
            _3276.CylindricalGearSetSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3277.CylindricalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3277,
        )

        return self.__parent__._cast(
            _3277.CylindricalGearSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3278.CylindricalPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3278,
        )

        return self.__parent__._cast(
            _3278.CylindricalPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def datum_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3279.DatumSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3279,
        )

        return self.__parent__._cast(_3279.DatumSteadyStateSynchronousResponse)

    @property
    def external_cad_model_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3281.ExternalCADModelSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3281,
        )

        return self.__parent__._cast(
            _3281.ExternalCADModelSteadyStateSynchronousResponse
        )

    @property
    def face_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3283.FaceGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3283,
        )

        return self.__parent__._cast(_3283.FaceGearSetSteadyStateSynchronousResponse)

    @property
    def face_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3284.FaceGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3284,
        )

        return self.__parent__._cast(_3284.FaceGearSteadyStateSynchronousResponse)

    @property
    def fe_part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3285.FEPartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3285,
        )

        return self.__parent__._cast(_3285.FEPartSteadyStateSynchronousResponse)

    @property
    def flexible_pin_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3286.FlexiblePinAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3286,
        )

        return self.__parent__._cast(
            _3286.FlexiblePinAssemblySteadyStateSynchronousResponse
        )

    @property
    def gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3288.GearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3288,
        )

        return self.__parent__._cast(_3288.GearSetSteadyStateSynchronousResponse)

    @property
    def gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3289.GearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3289,
        )

        return self.__parent__._cast(_3289.GearSteadyStateSynchronousResponse)

    @property
    def guide_dxf_model_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3290.GuideDxfModelSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3290,
        )

        return self.__parent__._cast(_3290.GuideDxfModelSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3292.HypoidGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3292,
        )

        return self.__parent__._cast(_3292.HypoidGearSetSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3293.HypoidGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3293,
        )

        return self.__parent__._cast(_3293.HypoidGearSteadyStateSynchronousResponse)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3296.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3296,
        )

        return self.__parent__._cast(
            _3296.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3297.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3297,
        )

        return self.__parent__._cast(
            _3297.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3299.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3299,
        )

        return self.__parent__._cast(
            _3299.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3300.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3300,
        )

        return self.__parent__._cast(
            _3300.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3302.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3302,
        )

        return self.__parent__._cast(
            _3302.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3303.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3303,
        )

        return self.__parent__._cast(
            _3303.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse
        )

    @property
    def mass_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3304.MassDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3304,
        )

        return self.__parent__._cast(_3304.MassDiscSteadyStateSynchronousResponse)

    @property
    def measurement_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3305.MeasurementComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3305,
        )

        return self.__parent__._cast(
            _3305.MeasurementComponentSteadyStateSynchronousResponse
        )

    @property
    def microphone_array_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3306.MicrophoneArraySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3306,
        )

        return self.__parent__._cast(
            _3306.MicrophoneArraySteadyStateSynchronousResponse
        )

    @property
    def microphone_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3307.MicrophoneSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3307,
        )

        return self.__parent__._cast(_3307.MicrophoneSteadyStateSynchronousResponse)

    @property
    def mountable_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3308.MountableComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3308,
        )

        return self.__parent__._cast(
            _3308.MountableComponentSteadyStateSynchronousResponse
        )

    @property
    def oil_seal_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3309.OilSealSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3309,
        )

        return self.__parent__._cast(_3309.OilSealSteadyStateSynchronousResponse)

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3310.PartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3310,
        )

        return self.__parent__._cast(_3310.PartSteadyStateSynchronousResponse)

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3312.PartToPartShearCouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3312,
        )

        return self.__parent__._cast(
            _3312.PartToPartShearCouplingHalfSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3313.PartToPartShearCouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3313,
        )

        return self.__parent__._cast(
            _3313.PartToPartShearCouplingSteadyStateSynchronousResponse
        )

    @property
    def planetary_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3315.PlanetaryGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3315,
        )

        return self.__parent__._cast(
            _3315.PlanetaryGearSetSteadyStateSynchronousResponse
        )

    @property
    def planet_carrier_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3316.PlanetCarrierSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3316,
        )

        return self.__parent__._cast(_3316.PlanetCarrierSteadyStateSynchronousResponse)

    @property
    def point_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3317.PointLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3317,
        )

        return self.__parent__._cast(_3317.PointLoadSteadyStateSynchronousResponse)

    @property
    def power_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3318.PowerLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3318,
        )

        return self.__parent__._cast(_3318.PowerLoadSteadyStateSynchronousResponse)

    @property
    def pulley_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3319.PulleySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3319,
        )

        return self.__parent__._cast(_3319.PulleySteadyStateSynchronousResponse)

    @property
    def ring_pins_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3320.RingPinsSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3320,
        )

        return self.__parent__._cast(_3320.RingPinsSteadyStateSynchronousResponse)

    @property
    def rolling_ring_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3322.RollingRingAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3322,
        )

        return self.__parent__._cast(
            _3322.RollingRingAssemblySteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3324.RollingRingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3324,
        )

        return self.__parent__._cast(_3324.RollingRingSteadyStateSynchronousResponse)

    @property
    def root_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3325.RootAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3325,
        )

        return self.__parent__._cast(_3325.RootAssemblySteadyStateSynchronousResponse)

    @property
    def shaft_hub_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3326.ShaftHubConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3326,
        )

        return self.__parent__._cast(
            _3326.ShaftHubConnectionSteadyStateSynchronousResponse
        )

    @property
    def shaft_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3327.ShaftSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3327,
        )

        return self.__parent__._cast(_3327.ShaftSteadyStateSynchronousResponse)

    @property
    def specialised_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3329.SpecialisedAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3329,
        )

        return self.__parent__._cast(
            _3329.SpecialisedAssemblySteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3331.SpiralBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3331,
        )

        return self.__parent__._cast(
            _3331.SpiralBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3332.SpiralBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3332,
        )

        return self.__parent__._cast(
            _3332.SpiralBevelGearSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3334.SpringDamperHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3334,
        )

        return self.__parent__._cast(
            _3334.SpringDamperHalfSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3335.SpringDamperSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3335,
        )

        return self.__parent__._cast(_3335.SpringDamperSteadyStateSynchronousResponse)

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3340.StraightBevelDiffGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3340,
        )

        return self.__parent__._cast(
            _3340.StraightBevelDiffGearSetSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3341.StraightBevelDiffGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3341,
        )

        return self.__parent__._cast(
            _3341.StraightBevelDiffGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3343.StraightBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3343,
        )

        return self.__parent__._cast(
            _3343.StraightBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3344.StraightBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3344,
        )

        return self.__parent__._cast(
            _3344.StraightBevelGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3345.StraightBevelPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3345,
        )

        return self.__parent__._cast(
            _3345.StraightBevelPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3346.StraightBevelSunGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3346,
        )

        return self.__parent__._cast(
            _3346.StraightBevelSunGearSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3347.SynchroniserHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3347,
        )

        return self.__parent__._cast(
            _3347.SynchroniserHalfSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3348.SynchroniserPartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3348,
        )

        return self.__parent__._cast(
            _3348.SynchroniserPartSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3349.SynchroniserSleeveSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3349,
        )

        return self.__parent__._cast(
            _3349.SynchroniserSleeveSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3350.SynchroniserSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3350,
        )

        return self.__parent__._cast(_3350.SynchroniserSteadyStateSynchronousResponse)

    @property
    def torque_converter_pump_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3352.TorqueConverterPumpSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3352,
        )

        return self.__parent__._cast(
            _3352.TorqueConverterPumpSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3353.TorqueConverterSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3353,
        )

        return self.__parent__._cast(
            _3353.TorqueConverterSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3354.TorqueConverterTurbineSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3354,
        )

        return self.__parent__._cast(
            _3354.TorqueConverterTurbineSteadyStateSynchronousResponse
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3355.UnbalancedMassSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3355,
        )

        return self.__parent__._cast(_3355.UnbalancedMassSteadyStateSynchronousResponse)

    @property
    def virtual_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3356.VirtualComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3356,
        )

        return self.__parent__._cast(
            _3356.VirtualComponentSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3358.WormGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3358,
        )

        return self.__parent__._cast(_3358.WormGearSetSteadyStateSynchronousResponse)

    @property
    def worm_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3359.WormGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3359,
        )

        return self.__parent__._cast(_3359.WormGearSteadyStateSynchronousResponse)

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3361.ZerolBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3361,
        )

        return self.__parent__._cast(
            _3361.ZerolBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3362.ZerolBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3362,
        )

        return self.__parent__._cast(_3362.ZerolBevelGearSteadyStateSynchronousResponse)

    @property
    def abstract_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3494.AbstractAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3494,
        )

        return self.__parent__._cast(
            _3494.AbstractAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_shaft_or_housing_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3495.AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3495,
        )

        return self.__parent__._cast(
            _3495.AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_shaft_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3496.AbstractShaftSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3496,
        )

        return self.__parent__._cast(
            _3496.AbstractShaftSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3499.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3499,
        )

        return self.__parent__._cast(
            _3499.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3500.AGMAGleasonConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3500,
        )

        return self.__parent__._cast(
            _3500.AGMAGleasonConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3501.AssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3501,
        )

        return self.__parent__._cast(
            _3501.AssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bearing_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3502.BearingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3502,
        )

        return self.__parent__._cast(
            _3502.BearingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def belt_drive_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3504.BeltDriveSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3504,
        )

        return self.__parent__._cast(
            _3504.BeltDriveSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3506.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3506,
        )

        return self.__parent__._cast(
            _3506.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3507.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3507,
        )

        return self.__parent__._cast(
            _3507.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3508.BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3508,
        )

        return self.__parent__._cast(
            _3508.BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3509.BevelDifferentialSunGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3509,
        )

        return self.__parent__._cast(
            _3509.BevelDifferentialSunGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3511.BevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3511,
        )

        return self.__parent__._cast(
            _3511.BevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3512.BevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3512,
        )

        return self.__parent__._cast(
            _3512.BevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bolted_joint_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3513.BoltedJointSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3513,
        )

        return self.__parent__._cast(
            _3513.BoltedJointSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bolt_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3514.BoltSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3514,
        )

        return self.__parent__._cast(_3514.BoltSteadyStateSynchronousResponseOnAShaft)

    @property
    def clutch_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3516.ClutchHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3516,
        )

        return self.__parent__._cast(
            _3516.ClutchHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def clutch_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3517.ClutchSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3517,
        )

        return self.__parent__._cast(_3517.ClutchSteadyStateSynchronousResponseOnAShaft)

    @property
    def component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3519.ComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3519,
        )

        return self.__parent__._cast(
            _3519.ComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3521.ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3521,
        )

        return self.__parent__._cast(
            _3521.ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3522.ConceptCouplingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3522,
        )

        return self.__parent__._cast(
            _3522.ConceptCouplingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3524.ConceptGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3524,
        )

        return self.__parent__._cast(
            _3524.ConceptGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3525.ConceptGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3525,
        )

        return self.__parent__._cast(
            _3525.ConceptGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3527.ConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3527,
        )

        return self.__parent__._cast(
            _3527.ConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3528.ConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3528,
        )

        return self.__parent__._cast(
            _3528.ConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connector_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3530.ConnectorSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3530,
        )

        return self.__parent__._cast(
            _3530.ConnectorSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3532.CouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3532,
        )

        return self.__parent__._cast(
            _3532.CouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3533.CouplingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3533,
        )

        return self.__parent__._cast(
            _3533.CouplingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_pulley_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3535.CVTPulleySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3535,
        )

        return self.__parent__._cast(
            _3535.CVTPulleySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3536.CVTSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3536,
        )

        return self.__parent__._cast(_3536.CVTSteadyStateSynchronousResponseOnAShaft)

    @property
    def cycloidal_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3537.CycloidalAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3537,
        )

        return self.__parent__._cast(
            _3537.CycloidalAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3540.CycloidalDiscSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3540,
        )

        return self.__parent__._cast(
            _3540.CycloidalDiscSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3542.CylindricalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3542,
        )

        return self.__parent__._cast(
            _3542.CylindricalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3543.CylindricalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3543,
        )

        return self.__parent__._cast(
            _3543.CylindricalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3544.CylindricalPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3544,
        )

        return self.__parent__._cast(
            _3544.CylindricalPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def datum_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3545.DatumSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3545,
        )

        return self.__parent__._cast(_3545.DatumSteadyStateSynchronousResponseOnAShaft)

    @property
    def external_cad_model_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3546.ExternalCADModelSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3546,
        )

        return self.__parent__._cast(
            _3546.ExternalCADModelSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3548.FaceGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3548,
        )

        return self.__parent__._cast(
            _3548.FaceGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3549.FaceGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3549,
        )

        return self.__parent__._cast(
            _3549.FaceGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def fe_part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3550.FEPartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3550,
        )

        return self.__parent__._cast(_3550.FEPartSteadyStateSynchronousResponseOnAShaft)

    @property
    def flexible_pin_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3551.FlexiblePinAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3551,
        )

        return self.__parent__._cast(
            _3551.FlexiblePinAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3553.GearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3553,
        )

        return self.__parent__._cast(
            _3553.GearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3554.GearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3554,
        )

        return self.__parent__._cast(_3554.GearSteadyStateSynchronousResponseOnAShaft)

    @property
    def guide_dxf_model_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3555.GuideDxfModelSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3555,
        )

        return self.__parent__._cast(
            _3555.GuideDxfModelSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3557.HypoidGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3557,
        )

        return self.__parent__._cast(
            _3557.HypoidGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3558.HypoidGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3558,
        )

        return self.__parent__._cast(
            _3558.HypoidGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3561.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3561,
        )

        return self.__parent__._cast(
            _3561.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3562.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3562,
        )

        return self.__parent__._cast(
            _3562.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3564.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3564,
        )

        return self.__parent__._cast(
            _3564.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3565.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3565,
        )

        return self.__parent__._cast(
            _3565.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3567.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3567,
        )

        return self.__parent__._cast(
            _3567.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3568.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3568,
        )

        return self.__parent__._cast(
            _3568.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def mass_disc_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3569.MassDiscSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3569,
        )

        return self.__parent__._cast(
            _3569.MassDiscSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def measurement_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3570.MeasurementComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3570,
        )

        return self.__parent__._cast(
            _3570.MeasurementComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def microphone_array_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3571.MicrophoneArraySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3571,
        )

        return self.__parent__._cast(
            _3571.MicrophoneArraySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def microphone_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3572.MicrophoneSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3572,
        )

        return self.__parent__._cast(
            _3572.MicrophoneSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def mountable_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3573.MountableComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3573,
        )

        return self.__parent__._cast(
            _3573.MountableComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def oil_seal_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3574.OilSealSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3574,
        )

        return self.__parent__._cast(
            _3574.OilSealSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3575.PartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3575,
        )

        return self.__parent__._cast(_3575.PartSteadyStateSynchronousResponseOnAShaft)

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3577.PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3577,
        )

        return self.__parent__._cast(
            _3577.PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_to_part_shear_coupling_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3578.PartToPartShearCouplingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3578,
        )

        return self.__parent__._cast(
            _3578.PartToPartShearCouplingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planetary_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3580.PlanetaryGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3580,
        )

        return self.__parent__._cast(
            _3580.PlanetaryGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planet_carrier_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3581.PlanetCarrierSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3581,
        )

        return self.__parent__._cast(
            _3581.PlanetCarrierSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def point_load_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3582.PointLoadSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3582,
        )

        return self.__parent__._cast(
            _3582.PointLoadSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def power_load_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3583.PowerLoadSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3583,
        )

        return self.__parent__._cast(
            _3583.PowerLoadSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def pulley_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3584.PulleySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3584,
        )

        return self.__parent__._cast(_3584.PulleySteadyStateSynchronousResponseOnAShaft)

    @property
    def ring_pins_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3585.RingPinsSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3585,
        )

        return self.__parent__._cast(
            _3585.RingPinsSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3587.RollingRingAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3587,
        )

        return self.__parent__._cast(
            _3587.RollingRingAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3589.RollingRingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3589,
        )

        return self.__parent__._cast(
            _3589.RollingRingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def root_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3590.RootAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3590,
        )

        return self.__parent__._cast(
            _3590.RootAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_hub_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3591.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3591,
        )

        return self.__parent__._cast(
            _3591.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3592.ShaftSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3592,
        )

        return self.__parent__._cast(_3592.ShaftSteadyStateSynchronousResponseOnAShaft)

    @property
    def specialised_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3594.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3594,
        )

        return self.__parent__._cast(
            _3594.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3596.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3596,
        )

        return self.__parent__._cast(
            _3596.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3597.SpiralBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3597,
        )

        return self.__parent__._cast(
            _3597.SpiralBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3599.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3599,
        )

        return self.__parent__._cast(
            _3599.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3600.SpringDamperSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3600,
        )

        return self.__parent__._cast(
            _3600.SpringDamperSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3603.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3603,
        )

        return self.__parent__._cast(
            _3603.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3604.StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3604,
        )

        return self.__parent__._cast(
            _3604.StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3606.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3606,
        )

        return self.__parent__._cast(
            _3606.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3607.StraightBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3607,
        )

        return self.__parent__._cast(
            _3607.StraightBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3608.StraightBevelPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3608,
        )

        return self.__parent__._cast(
            _3608.StraightBevelPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3609.StraightBevelSunGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3609,
        )

        return self.__parent__._cast(
            _3609.StraightBevelSunGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3610.SynchroniserHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3610,
        )

        return self.__parent__._cast(
            _3610.SynchroniserHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3611.SynchroniserPartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3611,
        )

        return self.__parent__._cast(
            _3611.SynchroniserPartSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3612.SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3612,
        )

        return self.__parent__._cast(
            _3612.SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3613.SynchroniserSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3613,
        )

        return self.__parent__._cast(
            _3613.SynchroniserSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_pump_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3615.TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3615,
        )

        return self.__parent__._cast(
            _3615.TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3616.TorqueConverterSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3616,
        )

        return self.__parent__._cast(
            _3616.TorqueConverterSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3617.TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3617,
        )

        return self.__parent__._cast(
            _3617.TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3618.UnbalancedMassSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3618,
        )

        return self.__parent__._cast(
            _3618.UnbalancedMassSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def virtual_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3619.VirtualComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3619,
        )

        return self.__parent__._cast(
            _3619.VirtualComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3621.WormGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3621,
        )

        return self.__parent__._cast(
            _3621.WormGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3622.WormGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3622,
        )

        return self.__parent__._cast(
            _3622.WormGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3624.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3624,
        )

        return self.__parent__._cast(
            _3624.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3625.ZerolBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3625,
        )

        return self.__parent__._cast(
            _3625.ZerolBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3757.AbstractAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3757,
        )

        return self.__parent__._cast(
            _3757.AbstractAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_or_housing_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3758.AbstractShaftOrHousingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3758,
        )

        return self.__parent__._cast(
            _3758.AbstractShaftOrHousingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3759.AbstractShaftSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3759,
        )

        return self.__parent__._cast(
            _3759.AbstractShaftSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3762.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3762,
        )

        return self.__parent__._cast(
            _3762.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3763.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3763,
        )

        return self.__parent__._cast(
            _3763.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3764.AssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3764,
        )

        return self.__parent__._cast(
            _3764.AssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bearing_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3765.BearingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3765,
        )

        return self.__parent__._cast(
            _3765.BearingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def belt_drive_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3767.BeltDriveSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3767,
        )

        return self.__parent__._cast(
            _3767.BeltDriveSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3769.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3769,
        )

        return self.__parent__._cast(
            _3769.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3770.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3770,
        )

        return self.__parent__._cast(
            _3770.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3771.BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3771,
        )

        return self.__parent__._cast(
            _3771.BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3772.BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3772,
        )

        return self.__parent__._cast(
            _3772.BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3774.BevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3774,
        )

        return self.__parent__._cast(
            _3774.BevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3775.BevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3775,
        )

        return self.__parent__._cast(
            _3775.BevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bolted_joint_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3776.BoltedJointSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3776,
        )

        return self.__parent__._cast(
            _3776.BoltedJointSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bolt_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3777.BoltSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3777,
        )

        return self.__parent__._cast(_3777.BoltSteadyStateSynchronousResponseAtASpeed)

    @property
    def clutch_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3779.ClutchHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3779,
        )

        return self.__parent__._cast(
            _3779.ClutchHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def clutch_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3780.ClutchSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3780,
        )

        return self.__parent__._cast(_3780.ClutchSteadyStateSynchronousResponseAtASpeed)

    @property
    def component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3782.ComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3782,
        )

        return self.__parent__._cast(
            _3782.ComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3784.ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3784,
        )

        return self.__parent__._cast(
            _3784.ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3785.ConceptCouplingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3785,
        )

        return self.__parent__._cast(
            _3785.ConceptCouplingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3787.ConceptGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3787,
        )

        return self.__parent__._cast(
            _3787.ConceptGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3788.ConceptGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3788,
        )

        return self.__parent__._cast(
            _3788.ConceptGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3790.ConicalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3790,
        )

        return self.__parent__._cast(
            _3790.ConicalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3791.ConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3791,
        )

        return self.__parent__._cast(
            _3791.ConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connector_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3793.ConnectorSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3793,
        )

        return self.__parent__._cast(
            _3793.ConnectorSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3795.CouplingHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3795,
        )

        return self.__parent__._cast(
            _3795.CouplingHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3796.CouplingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3796,
        )

        return self.__parent__._cast(
            _3796.CouplingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_pulley_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3798.CVTPulleySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3798,
        )

        return self.__parent__._cast(
            _3798.CVTPulleySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3799.CVTSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3799,
        )

        return self.__parent__._cast(_3799.CVTSteadyStateSynchronousResponseAtASpeed)

    @property
    def cycloidal_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3800.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3800,
        )

        return self.__parent__._cast(
            _3800.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3803.CycloidalDiscSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3803,
        )

        return self.__parent__._cast(
            _3803.CycloidalDiscSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3805.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3805,
        )

        return self.__parent__._cast(
            _3805.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3806.CylindricalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3806,
        )

        return self.__parent__._cast(
            _3806.CylindricalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3807.CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3807,
        )

        return self.__parent__._cast(
            _3807.CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def datum_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3808.DatumSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3808,
        )

        return self.__parent__._cast(_3808.DatumSteadyStateSynchronousResponseAtASpeed)

    @property
    def external_cad_model_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3809.ExternalCADModelSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3809,
        )

        return self.__parent__._cast(
            _3809.ExternalCADModelSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3811.FaceGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3811,
        )

        return self.__parent__._cast(
            _3811.FaceGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3812.FaceGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3812,
        )

        return self.__parent__._cast(
            _3812.FaceGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def fe_part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3813.FEPartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3813,
        )

        return self.__parent__._cast(_3813.FEPartSteadyStateSynchronousResponseAtASpeed)

    @property
    def flexible_pin_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3814.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3814,
        )

        return self.__parent__._cast(
            _3814.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3816.GearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3816,
        )

        return self.__parent__._cast(
            _3816.GearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3817.GearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3817,
        )

        return self.__parent__._cast(_3817.GearSteadyStateSynchronousResponseAtASpeed)

    @property
    def guide_dxf_model_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3818.GuideDxfModelSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3818,
        )

        return self.__parent__._cast(
            _3818.GuideDxfModelSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3820.HypoidGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3820,
        )

        return self.__parent__._cast(
            _3820.HypoidGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3821.HypoidGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3821,
        )

        return self.__parent__._cast(
            _3821.HypoidGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3824.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3824,
        )

        return self.__parent__._cast(
            _3824.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3825.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3825,
        )

        return self.__parent__._cast(
            _3825.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3827.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3827,
        )

        return self.__parent__._cast(
            _3827.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3828.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3828,
        )

        return self.__parent__._cast(
            _3828.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3830.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3830,
        )

        return self.__parent__._cast(
            _3830.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3831.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3831,
        )

        return self.__parent__._cast(
            _3831.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def mass_disc_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3832.MassDiscSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3832,
        )

        return self.__parent__._cast(
            _3832.MassDiscSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def measurement_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3833.MeasurementComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3833,
        )

        return self.__parent__._cast(
            _3833.MeasurementComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def microphone_array_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3834.MicrophoneArraySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3834,
        )

        return self.__parent__._cast(
            _3834.MicrophoneArraySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def microphone_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3835.MicrophoneSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3835,
        )

        return self.__parent__._cast(
            _3835.MicrophoneSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def mountable_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3836.MountableComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3836,
        )

        return self.__parent__._cast(
            _3836.MountableComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def oil_seal_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3837.OilSealSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3837,
        )

        return self.__parent__._cast(
            _3837.OilSealSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3838.PartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3838,
        )

        return self.__parent__._cast(_3838.PartSteadyStateSynchronousResponseAtASpeed)

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3840.PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3840,
        )

        return self.__parent__._cast(
            _3840.PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3841.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3841,
        )

        return self.__parent__._cast(
            _3841.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planetary_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3843.PlanetaryGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3843,
        )

        return self.__parent__._cast(
            _3843.PlanetaryGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planet_carrier_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3844.PlanetCarrierSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3844,
        )

        return self.__parent__._cast(
            _3844.PlanetCarrierSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def point_load_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3845.PointLoadSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3845,
        )

        return self.__parent__._cast(
            _3845.PointLoadSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def power_load_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3846.PowerLoadSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3846,
        )

        return self.__parent__._cast(
            _3846.PowerLoadSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def pulley_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3847.PulleySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3847,
        )

        return self.__parent__._cast(_3847.PulleySteadyStateSynchronousResponseAtASpeed)

    @property
    def ring_pins_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3848.RingPinsSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3848,
        )

        return self.__parent__._cast(
            _3848.RingPinsSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3850.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3850,
        )

        return self.__parent__._cast(
            _3850.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3852.RollingRingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3852,
        )

        return self.__parent__._cast(
            _3852.RollingRingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def root_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3853.RootAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3853,
        )

        return self.__parent__._cast(
            _3853.RootAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_hub_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3854.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3854,
        )

        return self.__parent__._cast(
            _3854.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3855.ShaftSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3855,
        )

        return self.__parent__._cast(_3855.ShaftSteadyStateSynchronousResponseAtASpeed)

    @property
    def specialised_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3857.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3857,
        )

        return self.__parent__._cast(
            _3857.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3859.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3859,
        )

        return self.__parent__._cast(
            _3859.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3860.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3860,
        )

        return self.__parent__._cast(
            _3860.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3862.SpringDamperHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3862,
        )

        return self.__parent__._cast(
            _3862.SpringDamperHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3863.SpringDamperSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3863,
        )

        return self.__parent__._cast(
            _3863.SpringDamperSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3866.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3866,
        )

        return self.__parent__._cast(
            _3866.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3867.StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3867,
        )

        return self.__parent__._cast(
            _3867.StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3869.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3869,
        )

        return self.__parent__._cast(
            _3869.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3870.StraightBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3870,
        )

        return self.__parent__._cast(
            _3870.StraightBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3871.StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3871,
        )

        return self.__parent__._cast(
            _3871.StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3872.StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3872,
        )

        return self.__parent__._cast(
            _3872.StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3873.SynchroniserHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3873,
        )

        return self.__parent__._cast(
            _3873.SynchroniserHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3874.SynchroniserPartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3874,
        )

        return self.__parent__._cast(
            _3874.SynchroniserPartSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3875.SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3875,
        )

        return self.__parent__._cast(
            _3875.SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3876.SynchroniserSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3876,
        )

        return self.__parent__._cast(
            _3876.SynchroniserSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_pump_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3878.TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3878,
        )

        return self.__parent__._cast(
            _3878.TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3879.TorqueConverterSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3879,
        )

        return self.__parent__._cast(
            _3879.TorqueConverterSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3880.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3880,
        )

        return self.__parent__._cast(
            _3880.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3881.UnbalancedMassSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3881,
        )

        return self.__parent__._cast(
            _3881.UnbalancedMassSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def virtual_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3882.VirtualComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3882,
        )

        return self.__parent__._cast(
            _3882.VirtualComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3884.WormGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3884,
        )

        return self.__parent__._cast(
            _3884.WormGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3885.WormGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3885,
        )

        return self.__parent__._cast(
            _3885.WormGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3887.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3887,
        )

        return self.__parent__._cast(
            _3887.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3888.ZerolBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3888,
        )

        return self.__parent__._cast(
            _3888.ZerolBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4020.AbstractAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4020,
        )

        return self.__parent__._cast(_4020.AbstractAssemblyStabilityAnalysis)

    @property
    def abstract_shaft_or_housing_stability_analysis(
        self: "CastSelf",
    ) -> "_4021.AbstractShaftOrHousingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4021,
        )

        return self.__parent__._cast(_4021.AbstractShaftOrHousingStabilityAnalysis)

    @property
    def abstract_shaft_stability_analysis(
        self: "CastSelf",
    ) -> "_4022.AbstractShaftStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4022,
        )

        return self.__parent__._cast(_4022.AbstractShaftStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4025.AGMAGleasonConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4025,
        )

        return self.__parent__._cast(_4025.AGMAGleasonConicalGearSetStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4026.AGMAGleasonConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4026,
        )

        return self.__parent__._cast(_4026.AGMAGleasonConicalGearStabilityAnalysis)

    @property
    def assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4027.AssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4027,
        )

        return self.__parent__._cast(_4027.AssemblyStabilityAnalysis)

    @property
    def bearing_stability_analysis(
        self: "CastSelf",
    ) -> "_4028.BearingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4028,
        )

        return self.__parent__._cast(_4028.BearingStabilityAnalysis)

    @property
    def belt_drive_stability_analysis(
        self: "CastSelf",
    ) -> "_4030.BeltDriveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4030,
        )

        return self.__parent__._cast(_4030.BeltDriveStabilityAnalysis)

    @property
    def bevel_differential_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4032.BevelDifferentialGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4032,
        )

        return self.__parent__._cast(_4032.BevelDifferentialGearSetStabilityAnalysis)

    @property
    def bevel_differential_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4033.BevelDifferentialGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4033,
        )

        return self.__parent__._cast(_4033.BevelDifferentialGearStabilityAnalysis)

    @property
    def bevel_differential_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4034.BevelDifferentialPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4034,
        )

        return self.__parent__._cast(_4034.BevelDifferentialPlanetGearStabilityAnalysis)

    @property
    def bevel_differential_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4035.BevelDifferentialSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4035,
        )

        return self.__parent__._cast(_4035.BevelDifferentialSunGearStabilityAnalysis)

    @property
    def bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4037.BevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4037,
        )

        return self.__parent__._cast(_4037.BevelGearSetStabilityAnalysis)

    @property
    def bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4038.BevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4038,
        )

        return self.__parent__._cast(_4038.BevelGearStabilityAnalysis)

    @property
    def bolted_joint_stability_analysis(
        self: "CastSelf",
    ) -> "_4039.BoltedJointStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4039,
        )

        return self.__parent__._cast(_4039.BoltedJointStabilityAnalysis)

    @property
    def bolt_stability_analysis(self: "CastSelf") -> "_4040.BoltStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4040,
        )

        return self.__parent__._cast(_4040.BoltStabilityAnalysis)

    @property
    def clutch_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4042.ClutchHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4042,
        )

        return self.__parent__._cast(_4042.ClutchHalfStabilityAnalysis)

    @property
    def clutch_stability_analysis(self: "CastSelf") -> "_4043.ClutchStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4043,
        )

        return self.__parent__._cast(_4043.ClutchStabilityAnalysis)

    @property
    def component_stability_analysis(
        self: "CastSelf",
    ) -> "_4045.ComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4045,
        )

        return self.__parent__._cast(_4045.ComponentStabilityAnalysis)

    @property
    def concept_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4047.ConceptCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4047,
        )

        return self.__parent__._cast(_4047.ConceptCouplingHalfStabilityAnalysis)

    @property
    def concept_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_4048.ConceptCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4048,
        )

        return self.__parent__._cast(_4048.ConceptCouplingStabilityAnalysis)

    @property
    def concept_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4050.ConceptGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4050,
        )

        return self.__parent__._cast(_4050.ConceptGearSetStabilityAnalysis)

    @property
    def concept_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4051.ConceptGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4051,
        )

        return self.__parent__._cast(_4051.ConceptGearStabilityAnalysis)

    @property
    def conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4053.ConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4053,
        )

        return self.__parent__._cast(_4053.ConicalGearSetStabilityAnalysis)

    @property
    def conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4054.ConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4054,
        )

        return self.__parent__._cast(_4054.ConicalGearStabilityAnalysis)

    @property
    def connector_stability_analysis(
        self: "CastSelf",
    ) -> "_4056.ConnectorStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4056,
        )

        return self.__parent__._cast(_4056.ConnectorStabilityAnalysis)

    @property
    def coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4058.CouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4058,
        )

        return self.__parent__._cast(_4058.CouplingHalfStabilityAnalysis)

    @property
    def coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_4059.CouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4059,
        )

        return self.__parent__._cast(_4059.CouplingStabilityAnalysis)

    @property
    def cvt_pulley_stability_analysis(
        self: "CastSelf",
    ) -> "_4062.CVTPulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4062,
        )

        return self.__parent__._cast(_4062.CVTPulleyStabilityAnalysis)

    @property
    def cvt_stability_analysis(self: "CastSelf") -> "_4063.CVTStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4063,
        )

        return self.__parent__._cast(_4063.CVTStabilityAnalysis)

    @property
    def cycloidal_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4064.CycloidalAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4064,
        )

        return self.__parent__._cast(_4064.CycloidalAssemblyStabilityAnalysis)

    @property
    def cycloidal_disc_stability_analysis(
        self: "CastSelf",
    ) -> "_4067.CycloidalDiscStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4067,
        )

        return self.__parent__._cast(_4067.CycloidalDiscStabilityAnalysis)

    @property
    def cylindrical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4069.CylindricalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4069,
        )

        return self.__parent__._cast(_4069.CylindricalGearSetStabilityAnalysis)

    @property
    def cylindrical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4070.CylindricalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4070,
        )

        return self.__parent__._cast(_4070.CylindricalGearStabilityAnalysis)

    @property
    def cylindrical_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4071.CylindricalPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4071,
        )

        return self.__parent__._cast(_4071.CylindricalPlanetGearStabilityAnalysis)

    @property
    def datum_stability_analysis(self: "CastSelf") -> "_4072.DatumStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4072,
        )

        return self.__parent__._cast(_4072.DatumStabilityAnalysis)

    @property
    def external_cad_model_stability_analysis(
        self: "CastSelf",
    ) -> "_4074.ExternalCADModelStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4074,
        )

        return self.__parent__._cast(_4074.ExternalCADModelStabilityAnalysis)

    @property
    def face_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4076.FaceGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4076,
        )

        return self.__parent__._cast(_4076.FaceGearSetStabilityAnalysis)

    @property
    def face_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4077.FaceGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4077,
        )

        return self.__parent__._cast(_4077.FaceGearStabilityAnalysis)

    @property
    def fe_part_stability_analysis(self: "CastSelf") -> "_4078.FEPartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4078,
        )

        return self.__parent__._cast(_4078.FEPartStabilityAnalysis)

    @property
    def flexible_pin_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4079.FlexiblePinAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4079,
        )

        return self.__parent__._cast(_4079.FlexiblePinAssemblyStabilityAnalysis)

    @property
    def gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4081.GearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4081,
        )

        return self.__parent__._cast(_4081.GearSetStabilityAnalysis)

    @property
    def gear_stability_analysis(self: "CastSelf") -> "_4082.GearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4082,
        )

        return self.__parent__._cast(_4082.GearStabilityAnalysis)

    @property
    def guide_dxf_model_stability_analysis(
        self: "CastSelf",
    ) -> "_4083.GuideDxfModelStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4083,
        )

        return self.__parent__._cast(_4083.GuideDxfModelStabilityAnalysis)

    @property
    def hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4085.HypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4085,
        )

        return self.__parent__._cast(_4085.HypoidGearSetStabilityAnalysis)

    @property
    def hypoid_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4086.HypoidGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4086,
        )

        return self.__parent__._cast(_4086.HypoidGearStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4089.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4089,
        )

        return self.__parent__._cast(
            _4089.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4090.KlingelnbergCycloPalloidConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4090,
        )

        return self.__parent__._cast(
            _4090.KlingelnbergCycloPalloidConicalGearStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4092.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4092,
        )

        return self.__parent__._cast(
            _4092.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4093.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4093,
        )

        return self.__parent__._cast(
            _4093.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4095.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4095,
        )

        return self.__parent__._cast(
            _4095.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4096.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4096,
        )

        return self.__parent__._cast(
            _4096.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis
        )

    @property
    def mass_disc_stability_analysis(
        self: "CastSelf",
    ) -> "_4097.MassDiscStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4097,
        )

        return self.__parent__._cast(_4097.MassDiscStabilityAnalysis)

    @property
    def measurement_component_stability_analysis(
        self: "CastSelf",
    ) -> "_4098.MeasurementComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4098,
        )

        return self.__parent__._cast(_4098.MeasurementComponentStabilityAnalysis)

    @property
    def microphone_array_stability_analysis(
        self: "CastSelf",
    ) -> "_4099.MicrophoneArrayStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4099,
        )

        return self.__parent__._cast(_4099.MicrophoneArrayStabilityAnalysis)

    @property
    def microphone_stability_analysis(
        self: "CastSelf",
    ) -> "_4100.MicrophoneStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4100,
        )

        return self.__parent__._cast(_4100.MicrophoneStabilityAnalysis)

    @property
    def mountable_component_stability_analysis(
        self: "CastSelf",
    ) -> "_4101.MountableComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4101,
        )

        return self.__parent__._cast(_4101.MountableComponentStabilityAnalysis)

    @property
    def oil_seal_stability_analysis(
        self: "CastSelf",
    ) -> "_4102.OilSealStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4102,
        )

        return self.__parent__._cast(_4102.OilSealStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "_4103.PartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4103,
        )

        return self.__parent__._cast(_4103.PartStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4105.PartToPartShearCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4105,
        )

        return self.__parent__._cast(_4105.PartToPartShearCouplingHalfStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_4106.PartToPartShearCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4106,
        )

        return self.__parent__._cast(_4106.PartToPartShearCouplingStabilityAnalysis)

    @property
    def planetary_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4108.PlanetaryGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4108,
        )

        return self.__parent__._cast(_4108.PlanetaryGearSetStabilityAnalysis)

    @property
    def planet_carrier_stability_analysis(
        self: "CastSelf",
    ) -> "_4109.PlanetCarrierStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4109,
        )

        return self.__parent__._cast(_4109.PlanetCarrierStabilityAnalysis)

    @property
    def point_load_stability_analysis(
        self: "CastSelf",
    ) -> "_4110.PointLoadStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4110,
        )

        return self.__parent__._cast(_4110.PointLoadStabilityAnalysis)

    @property
    def power_load_stability_analysis(
        self: "CastSelf",
    ) -> "_4111.PowerLoadStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4111,
        )

        return self.__parent__._cast(_4111.PowerLoadStabilityAnalysis)

    @property
    def pulley_stability_analysis(self: "CastSelf") -> "_4112.PulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4112,
        )

        return self.__parent__._cast(_4112.PulleyStabilityAnalysis)

    @property
    def ring_pins_stability_analysis(
        self: "CastSelf",
    ) -> "_4113.RingPinsStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4113,
        )

        return self.__parent__._cast(_4113.RingPinsStabilityAnalysis)

    @property
    def rolling_ring_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4115.RollingRingAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4115,
        )

        return self.__parent__._cast(_4115.RollingRingAssemblyStabilityAnalysis)

    @property
    def rolling_ring_stability_analysis(
        self: "CastSelf",
    ) -> "_4117.RollingRingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4117,
        )

        return self.__parent__._cast(_4117.RollingRingStabilityAnalysis)

    @property
    def root_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4118.RootAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4118,
        )

        return self.__parent__._cast(_4118.RootAssemblyStabilityAnalysis)

    @property
    def shaft_hub_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4119.ShaftHubConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4119,
        )

        return self.__parent__._cast(_4119.ShaftHubConnectionStabilityAnalysis)

    @property
    def shaft_stability_analysis(self: "CastSelf") -> "_4120.ShaftStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4120,
        )

        return self.__parent__._cast(_4120.ShaftStabilityAnalysis)

    @property
    def specialised_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4122.SpecialisedAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4122,
        )

        return self.__parent__._cast(_4122.SpecialisedAssemblyStabilityAnalysis)

    @property
    def spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4124.SpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4124,
        )

        return self.__parent__._cast(_4124.SpiralBevelGearSetStabilityAnalysis)

    @property
    def spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4125.SpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4125,
        )

        return self.__parent__._cast(_4125.SpiralBevelGearStabilityAnalysis)

    @property
    def spring_damper_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4127.SpringDamperHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4127,
        )

        return self.__parent__._cast(_4127.SpringDamperHalfStabilityAnalysis)

    @property
    def spring_damper_stability_analysis(
        self: "CastSelf",
    ) -> "_4128.SpringDamperStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4128,
        )

        return self.__parent__._cast(_4128.SpringDamperStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4133.StraightBevelDiffGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4133,
        )

        return self.__parent__._cast(_4133.StraightBevelDiffGearSetStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4134.StraightBevelDiffGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4134,
        )

        return self.__parent__._cast(_4134.StraightBevelDiffGearStabilityAnalysis)

    @property
    def straight_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4136.StraightBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4136,
        )

        return self.__parent__._cast(_4136.StraightBevelGearSetStabilityAnalysis)

    @property
    def straight_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4137.StraightBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4137,
        )

        return self.__parent__._cast(_4137.StraightBevelGearStabilityAnalysis)

    @property
    def straight_bevel_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4138.StraightBevelPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4138,
        )

        return self.__parent__._cast(_4138.StraightBevelPlanetGearStabilityAnalysis)

    @property
    def straight_bevel_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4139.StraightBevelSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4139,
        )

        return self.__parent__._cast(_4139.StraightBevelSunGearStabilityAnalysis)

    @property
    def synchroniser_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4140.SynchroniserHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4140,
        )

        return self.__parent__._cast(_4140.SynchroniserHalfStabilityAnalysis)

    @property
    def synchroniser_part_stability_analysis(
        self: "CastSelf",
    ) -> "_4141.SynchroniserPartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4141,
        )

        return self.__parent__._cast(_4141.SynchroniserPartStabilityAnalysis)

    @property
    def synchroniser_sleeve_stability_analysis(
        self: "CastSelf",
    ) -> "_4142.SynchroniserSleeveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4142,
        )

        return self.__parent__._cast(_4142.SynchroniserSleeveStabilityAnalysis)

    @property
    def synchroniser_stability_analysis(
        self: "CastSelf",
    ) -> "_4143.SynchroniserStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4143,
        )

        return self.__parent__._cast(_4143.SynchroniserStabilityAnalysis)

    @property
    def torque_converter_pump_stability_analysis(
        self: "CastSelf",
    ) -> "_4145.TorqueConverterPumpStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4145,
        )

        return self.__parent__._cast(_4145.TorqueConverterPumpStabilityAnalysis)

    @property
    def torque_converter_stability_analysis(
        self: "CastSelf",
    ) -> "_4146.TorqueConverterStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4146,
        )

        return self.__parent__._cast(_4146.TorqueConverterStabilityAnalysis)

    @property
    def torque_converter_turbine_stability_analysis(
        self: "CastSelf",
    ) -> "_4147.TorqueConverterTurbineStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4147,
        )

        return self.__parent__._cast(_4147.TorqueConverterTurbineStabilityAnalysis)

    @property
    def unbalanced_mass_stability_analysis(
        self: "CastSelf",
    ) -> "_4148.UnbalancedMassStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4148,
        )

        return self.__parent__._cast(_4148.UnbalancedMassStabilityAnalysis)

    @property
    def virtual_component_stability_analysis(
        self: "CastSelf",
    ) -> "_4149.VirtualComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4149,
        )

        return self.__parent__._cast(_4149.VirtualComponentStabilityAnalysis)

    @property
    def worm_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4151.WormGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4151,
        )

        return self.__parent__._cast(_4151.WormGearSetStabilityAnalysis)

    @property
    def worm_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4152.WormGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4152,
        )

        return self.__parent__._cast(_4152.WormGearStabilityAnalysis)

    @property
    def zerol_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4154.ZerolBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4154,
        )

        return self.__parent__._cast(_4154.ZerolBevelGearSetStabilityAnalysis)

    @property
    def zerol_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4155.ZerolBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4155,
        )

        return self.__parent__._cast(_4155.ZerolBevelGearStabilityAnalysis)

    @property
    def abstract_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4293.AbstractAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4293

        return self.__parent__._cast(_4293.AbstractAssemblyPowerFlow)

    @property
    def abstract_shaft_or_housing_power_flow(
        self: "CastSelf",
    ) -> "_4294.AbstractShaftOrHousingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4294

        return self.__parent__._cast(_4294.AbstractShaftOrHousingPowerFlow)

    @property
    def abstract_shaft_power_flow(self: "CastSelf") -> "_4295.AbstractShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4295

        return self.__parent__._cast(_4295.AbstractShaftPowerFlow)

    @property
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4298.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4298

        return self.__parent__._cast(_4298.AGMAGleasonConicalGearPowerFlow)

    @property
    def agma_gleason_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4299.AGMAGleasonConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4299

        return self.__parent__._cast(_4299.AGMAGleasonConicalGearSetPowerFlow)

    @property
    def assembly_power_flow(self: "CastSelf") -> "_4300.AssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4300

        return self.__parent__._cast(_4300.AssemblyPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4301.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4301

        return self.__parent__._cast(_4301.BearingPowerFlow)

    @property
    def belt_drive_power_flow(self: "CastSelf") -> "_4303.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4303

        return self.__parent__._cast(_4303.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4305.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4305

        return self.__parent__._cast(_4305.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4306.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4306

        return self.__parent__._cast(_4306.BevelDifferentialGearSetPowerFlow)

    @property
    def bevel_differential_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4307.BevelDifferentialPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4307

        return self.__parent__._cast(_4307.BevelDifferentialPlanetGearPowerFlow)

    @property
    def bevel_differential_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4308.BevelDifferentialSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4308

        return self.__parent__._cast(_4308.BevelDifferentialSunGearPowerFlow)

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4310.BevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4310

        return self.__parent__._cast(_4310.BevelGearPowerFlow)

    @property
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4311.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4311

        return self.__parent__._cast(_4311.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4312.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4312

        return self.__parent__._cast(_4312.BoltedJointPowerFlow)

    @property
    def bolt_power_flow(self: "CastSelf") -> "_4313.BoltPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4313

        return self.__parent__._cast(_4313.BoltPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4315.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4315

        return self.__parent__._cast(_4315.ClutchHalfPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4316.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4316

        return self.__parent__._cast(_4316.ClutchPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4318.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4318

        return self.__parent__._cast(_4318.ComponentPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4320.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4320

        return self.__parent__._cast(_4320.ConceptCouplingHalfPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4321.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4321

        return self.__parent__._cast(_4321.ConceptCouplingPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4323.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4323

        return self.__parent__._cast(_4323.ConceptGearPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4324.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4324

        return self.__parent__._cast(_4324.ConceptGearSetPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4326.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4326

        return self.__parent__._cast(_4326.ConicalGearPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4327.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4327

        return self.__parent__._cast(_4327.ConicalGearSetPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4329.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4329

        return self.__parent__._cast(_4329.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4331.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4331

        return self.__parent__._cast(_4331.CouplingHalfPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4332.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4332

        return self.__parent__._cast(_4332.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4334.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4334

        return self.__parent__._cast(_4334.CVTPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4335.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4335

        return self.__parent__._cast(_4335.CVTPulleyPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4336.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4336

        return self.__parent__._cast(_4336.CycloidalAssemblyPowerFlow)

    @property
    def cycloidal_disc_power_flow(self: "CastSelf") -> "_4339.CycloidalDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4339

        return self.__parent__._cast(_4339.CycloidalDiscPowerFlow)

    @property
    def cylindrical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4342.CylindricalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4342

        return self.__parent__._cast(_4342.CylindricalGearPowerFlow)

    @property
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4343.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4343

        return self.__parent__._cast(_4343.CylindricalGearSetPowerFlow)

    @property
    def cylindrical_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4344.CylindricalPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4344

        return self.__parent__._cast(_4344.CylindricalPlanetGearPowerFlow)

    @property
    def datum_power_flow(self: "CastSelf") -> "_4345.DatumPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4345

        return self.__parent__._cast(_4345.DatumPowerFlow)

    @property
    def external_cad_model_power_flow(
        self: "CastSelf",
    ) -> "_4346.ExternalCADModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4346

        return self.__parent__._cast(_4346.ExternalCADModelPowerFlow)

    @property
    def face_gear_power_flow(self: "CastSelf") -> "_4348.FaceGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4348

        return self.__parent__._cast(_4348.FaceGearPowerFlow)

    @property
    def face_gear_set_power_flow(self: "CastSelf") -> "_4349.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4349

        return self.__parent__._cast(_4349.FaceGearSetPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4352.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4352

        return self.__parent__._cast(_4352.FEPartPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4353.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4353

        return self.__parent__._cast(_4353.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4355.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4355

        return self.__parent__._cast(_4355.GearPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4356.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4356

        return self.__parent__._cast(_4356.GearSetPowerFlow)

    @property
    def guide_dxf_model_power_flow(self: "CastSelf") -> "_4357.GuideDxfModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4357

        return self.__parent__._cast(_4357.GuideDxfModelPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4359.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4359

        return self.__parent__._cast(_4359.HypoidGearPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4360.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4360

        return self.__parent__._cast(_4360.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4363.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4363

        return self.__parent__._cast(_4363.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4364.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4364

        return self.__parent__._cast(
            _4364.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4366.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4366

        return self.__parent__._cast(_4366.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4367.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4367

        return self.__parent__._cast(
            _4367.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4369.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4369

        return self.__parent__._cast(
            _4369.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4370.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4370

        return self.__parent__._cast(
            _4370.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        )

    @property
    def mass_disc_power_flow(self: "CastSelf") -> "_4371.MassDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4371

        return self.__parent__._cast(_4371.MassDiscPowerFlow)

    @property
    def measurement_component_power_flow(
        self: "CastSelf",
    ) -> "_4372.MeasurementComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4372

        return self.__parent__._cast(_4372.MeasurementComponentPowerFlow)

    @property
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4373.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4373

        return self.__parent__._cast(_4373.MicrophoneArrayPowerFlow)

    @property
    def microphone_power_flow(self: "CastSelf") -> "_4374.MicrophonePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4374

        return self.__parent__._cast(_4374.MicrophonePowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4375.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4375

        return self.__parent__._cast(_4375.MountableComponentPowerFlow)

    @property
    def oil_seal_power_flow(self: "CastSelf") -> "_4376.OilSealPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4376

        return self.__parent__._cast(_4376.OilSealPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4377.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4377

        return self.__parent__._cast(_4377.PartPowerFlow)

    @property
    def part_to_part_shear_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4379.PartToPartShearCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4379

        return self.__parent__._cast(_4379.PartToPartShearCouplingHalfPowerFlow)

    @property
    def part_to_part_shear_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4380.PartToPartShearCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4380

        return self.__parent__._cast(_4380.PartToPartShearCouplingPowerFlow)

    @property
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4382.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4382

        return self.__parent__._cast(_4382.PlanetaryGearSetPowerFlow)

    @property
    def planet_carrier_power_flow(self: "CastSelf") -> "_4383.PlanetCarrierPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4383

        return self.__parent__._cast(_4383.PlanetCarrierPowerFlow)

    @property
    def point_load_power_flow(self: "CastSelf") -> "_4384.PointLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4384

        return self.__parent__._cast(_4384.PointLoadPowerFlow)

    @property
    def power_load_power_flow(self: "CastSelf") -> "_4387.PowerLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4387

        return self.__parent__._cast(_4387.PowerLoadPowerFlow)

    @property
    def pulley_power_flow(self: "CastSelf") -> "_4388.PulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4388

        return self.__parent__._cast(_4388.PulleyPowerFlow)

    @property
    def ring_pins_power_flow(self: "CastSelf") -> "_4389.RingPinsPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4389

        return self.__parent__._cast(_4389.RingPinsPowerFlow)

    @property
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4391.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4391

        return self.__parent__._cast(_4391.RollingRingAssemblyPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4393.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4393

        return self.__parent__._cast(_4393.RollingRingPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4394.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4394

        return self.__parent__._cast(_4394.RootAssemblyPowerFlow)

    @property
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "_4395.ShaftHubConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4395

        return self.__parent__._cast(_4395.ShaftHubConnectionPowerFlow)

    @property
    def shaft_power_flow(self: "CastSelf") -> "_4396.ShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4396

        return self.__parent__._cast(_4396.ShaftPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4398.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4398

        return self.__parent__._cast(_4398.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4400.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4400

        return self.__parent__._cast(_4400.SpiralBevelGearPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4401.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4401

        return self.__parent__._cast(_4401.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4403.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4403

        return self.__parent__._cast(_4403.SpringDamperHalfPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4404.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4404

        return self.__parent__._cast(_4404.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4406.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4406

        return self.__parent__._cast(_4406.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4407.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4407

        return self.__parent__._cast(_4407.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4409.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4409

        return self.__parent__._cast(_4409.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4410.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4410

        return self.__parent__._cast(_4410.StraightBevelGearSetPowerFlow)

    @property
    def straight_bevel_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4411.StraightBevelPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4411

        return self.__parent__._cast(_4411.StraightBevelPlanetGearPowerFlow)

    @property
    def straight_bevel_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4412.StraightBevelSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4412

        return self.__parent__._cast(_4412.StraightBevelSunGearPowerFlow)

    @property
    def synchroniser_half_power_flow(
        self: "CastSelf",
    ) -> "_4413.SynchroniserHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4413

        return self.__parent__._cast(_4413.SynchroniserHalfPowerFlow)

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4414.SynchroniserPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4414

        return self.__parent__._cast(_4414.SynchroniserPartPowerFlow)

    @property
    def synchroniser_power_flow(self: "CastSelf") -> "_4415.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4415

        return self.__parent__._cast(_4415.SynchroniserPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4416.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4416

        return self.__parent__._cast(_4416.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4419.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4419

        return self.__parent__._cast(_4419.TorqueConverterPowerFlow)

    @property
    def torque_converter_pump_power_flow(
        self: "CastSelf",
    ) -> "_4420.TorqueConverterPumpPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4420

        return self.__parent__._cast(_4420.TorqueConverterPumpPowerFlow)

    @property
    def torque_converter_turbine_power_flow(
        self: "CastSelf",
    ) -> "_4421.TorqueConverterTurbinePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4421

        return self.__parent__._cast(_4421.TorqueConverterTurbinePowerFlow)

    @property
    def unbalanced_mass_power_flow(self: "CastSelf") -> "_4422.UnbalancedMassPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4422

        return self.__parent__._cast(_4422.UnbalancedMassPowerFlow)

    @property
    def virtual_component_power_flow(
        self: "CastSelf",
    ) -> "_4423.VirtualComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4423

        return self.__parent__._cast(_4423.VirtualComponentPowerFlow)

    @property
    def worm_gear_power_flow(self: "CastSelf") -> "_4425.WormGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4425

        return self.__parent__._cast(_4425.WormGearPowerFlow)

    @property
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4426.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4426

        return self.__parent__._cast(_4426.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4428.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4428

        return self.__parent__._cast(_4428.ZerolBevelGearPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4429.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4429

        return self.__parent__._cast(_4429.ZerolBevelGearSetPowerFlow)

    @property
    def abstract_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4561.AbstractAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4561,
        )

        return self.__parent__._cast(_4561.AbstractAssemblyParametricStudyTool)

    @property
    def abstract_shaft_or_housing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4562.AbstractShaftOrHousingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4562,
        )

        return self.__parent__._cast(_4562.AbstractShaftOrHousingParametricStudyTool)

    @property
    def abstract_shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4563.AbstractShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4563,
        )

        return self.__parent__._cast(_4563.AbstractShaftParametricStudyTool)

    @property
    def agma_gleason_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4566.AGMAGleasonConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4566,
        )

        return self.__parent__._cast(_4566.AGMAGleasonConicalGearParametricStudyTool)

    @property
    def agma_gleason_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4567.AGMAGleasonConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4567,
        )

        return self.__parent__._cast(_4567.AGMAGleasonConicalGearSetParametricStudyTool)

    @property
    def assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4568.AssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4568,
        )

        return self.__parent__._cast(_4568.AssemblyParametricStudyTool)

    @property
    def bearing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4569.BearingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4569,
        )

        return self.__parent__._cast(_4569.BearingParametricStudyTool)

    @property
    def belt_drive_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4571.BeltDriveParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4571,
        )

        return self.__parent__._cast(_4571.BeltDriveParametricStudyTool)

    @property
    def bevel_differential_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4573.BevelDifferentialGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4573,
        )

        return self.__parent__._cast(_4573.BevelDifferentialGearParametricStudyTool)

    @property
    def bevel_differential_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4574.BevelDifferentialGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4574,
        )

        return self.__parent__._cast(_4574.BevelDifferentialGearSetParametricStudyTool)

    @property
    def bevel_differential_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4575.BevelDifferentialPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4575,
        )

        return self.__parent__._cast(
            _4575.BevelDifferentialPlanetGearParametricStudyTool
        )

    @property
    def bevel_differential_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4576.BevelDifferentialSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4576,
        )

        return self.__parent__._cast(_4576.BevelDifferentialSunGearParametricStudyTool)

    @property
    def bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4578.BevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4578,
        )

        return self.__parent__._cast(_4578.BevelGearParametricStudyTool)

    @property
    def bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4579.BevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4579,
        )

        return self.__parent__._cast(_4579.BevelGearSetParametricStudyTool)

    @property
    def bolted_joint_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4580.BoltedJointParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4580,
        )

        return self.__parent__._cast(_4580.BoltedJointParametricStudyTool)

    @property
    def bolt_parametric_study_tool(self: "CastSelf") -> "_4581.BoltParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4581,
        )

        return self.__parent__._cast(_4581.BoltParametricStudyTool)

    @property
    def clutch_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4583.ClutchHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4583,
        )

        return self.__parent__._cast(_4583.ClutchHalfParametricStudyTool)

    @property
    def clutch_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4584.ClutchParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4584,
        )

        return self.__parent__._cast(_4584.ClutchParametricStudyTool)

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4586.ComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4586,
        )

        return self.__parent__._cast(_4586.ComponentParametricStudyTool)

    @property
    def concept_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4588.ConceptCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4588,
        )

        return self.__parent__._cast(_4588.ConceptCouplingHalfParametricStudyTool)

    @property
    def concept_coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4589.ConceptCouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4589,
        )

        return self.__parent__._cast(_4589.ConceptCouplingParametricStudyTool)

    @property
    def concept_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4591.ConceptGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4591,
        )

        return self.__parent__._cast(_4591.ConceptGearParametricStudyTool)

    @property
    def concept_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4592.ConceptGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4592,
        )

        return self.__parent__._cast(_4592.ConceptGearSetParametricStudyTool)

    @property
    def conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4594.ConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4594,
        )

        return self.__parent__._cast(_4594.ConicalGearParametricStudyTool)

    @property
    def conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4595.ConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4595,
        )

        return self.__parent__._cast(_4595.ConicalGearSetParametricStudyTool)

    @property
    def connector_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4597.ConnectorParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4597,
        )

        return self.__parent__._cast(_4597.ConnectorParametricStudyTool)

    @property
    def coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4599.CouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4599,
        )

        return self.__parent__._cast(_4599.CouplingHalfParametricStudyTool)

    @property
    def coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4600.CouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4600,
        )

        return self.__parent__._cast(_4600.CouplingParametricStudyTool)

    @property
    def cvt_parametric_study_tool(self: "CastSelf") -> "_4602.CVTParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4602,
        )

        return self.__parent__._cast(_4602.CVTParametricStudyTool)

    @property
    def cvt_pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4603.CVTPulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4603,
        )

        return self.__parent__._cast(_4603.CVTPulleyParametricStudyTool)

    @property
    def cycloidal_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4604.CycloidalAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4604,
        )

        return self.__parent__._cast(_4604.CycloidalAssemblyParametricStudyTool)

    @property
    def cycloidal_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4606.CycloidalDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4606,
        )

        return self.__parent__._cast(_4606.CycloidalDiscParametricStudyTool)

    @property
    def cylindrical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4609.CylindricalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4609,
        )

        return self.__parent__._cast(_4609.CylindricalGearParametricStudyTool)

    @property
    def cylindrical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4610.CylindricalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4610,
        )

        return self.__parent__._cast(_4610.CylindricalGearSetParametricStudyTool)

    @property
    def cylindrical_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4611.CylindricalPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4611,
        )

        return self.__parent__._cast(_4611.CylindricalPlanetGearParametricStudyTool)

    @property
    def datum_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4612.DatumParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4612,
        )

        return self.__parent__._cast(_4612.DatumParametricStudyTool)

    @property
    def external_cad_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4620.ExternalCADModelParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4620,
        )

        return self.__parent__._cast(_4620.ExternalCADModelParametricStudyTool)

    @property
    def face_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4622.FaceGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4622,
        )

        return self.__parent__._cast(_4622.FaceGearParametricStudyTool)

    @property
    def face_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4623.FaceGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4623,
        )

        return self.__parent__._cast(_4623.FaceGearSetParametricStudyTool)

    @property
    def fe_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4624.FEPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4624,
        )

        return self.__parent__._cast(_4624.FEPartParametricStudyTool)

    @property
    def flexible_pin_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4625.FlexiblePinAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4625,
        )

        return self.__parent__._cast(_4625.FlexiblePinAssemblyParametricStudyTool)

    @property
    def gear_parametric_study_tool(self: "CastSelf") -> "_4627.GearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4627,
        )

        return self.__parent__._cast(_4627.GearParametricStudyTool)

    @property
    def gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4628.GearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4628,
        )

        return self.__parent__._cast(_4628.GearSetParametricStudyTool)

    @property
    def guide_dxf_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4629.GuideDxfModelParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4629,
        )

        return self.__parent__._cast(_4629.GuideDxfModelParametricStudyTool)

    @property
    def hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4631.HypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4631,
        )

        return self.__parent__._cast(_4631.HypoidGearParametricStudyTool)

    @property
    def hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4632.HypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4632,
        )

        return self.__parent__._cast(_4632.HypoidGearSetParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4635.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4635,
        )

        return self.__parent__._cast(
            _4635.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4636.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4636,
        )

        return self.__parent__._cast(
            _4636.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4638.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4638,
        )

        return self.__parent__._cast(
            _4638.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4639.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4639,
        )

        return self.__parent__._cast(
            _4639.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4641.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4641,
        )

        return self.__parent__._cast(
            _4641.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4642.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4642,
        )

        return self.__parent__._cast(
            _4642.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
        )

    @property
    def mass_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4643.MassDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4643,
        )

        return self.__parent__._cast(_4643.MassDiscParametricStudyTool)

    @property
    def measurement_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4644.MeasurementComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4644,
        )

        return self.__parent__._cast(_4644.MeasurementComponentParametricStudyTool)

    @property
    def microphone_array_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4645.MicrophoneArrayParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4645,
        )

        return self.__parent__._cast(_4645.MicrophoneArrayParametricStudyTool)

    @property
    def microphone_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4646.MicrophoneParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4646,
        )

        return self.__parent__._cast(_4646.MicrophoneParametricStudyTool)

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4648.MountableComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4648,
        )

        return self.__parent__._cast(_4648.MountableComponentParametricStudyTool)

    @property
    def oil_seal_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4649.OilSealParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4649,
        )

        return self.__parent__._cast(_4649.OilSealParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4661.PartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4661,
        )

        return self.__parent__._cast(_4661.PartParametricStudyTool)

    @property
    def part_to_part_shear_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4663.PartToPartShearCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4663,
        )

        return self.__parent__._cast(
            _4663.PartToPartShearCouplingHalfParametricStudyTool
        )

    @property
    def part_to_part_shear_coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4664.PartToPartShearCouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4664,
        )

        return self.__parent__._cast(_4664.PartToPartShearCouplingParametricStudyTool)

    @property
    def planetary_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4666.PlanetaryGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4666,
        )

        return self.__parent__._cast(_4666.PlanetaryGearSetParametricStudyTool)

    @property
    def planet_carrier_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4667.PlanetCarrierParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4667,
        )

        return self.__parent__._cast(_4667.PlanetCarrierParametricStudyTool)

    @property
    def point_load_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4668.PointLoadParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4668,
        )

        return self.__parent__._cast(_4668.PointLoadParametricStudyTool)

    @property
    def power_load_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4669.PowerLoadParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4669,
        )

        return self.__parent__._cast(_4669.PowerLoadParametricStudyTool)

    @property
    def pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4670.PulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4670,
        )

        return self.__parent__._cast(_4670.PulleyParametricStudyTool)

    @property
    def ring_pins_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4671.RingPinsParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4671,
        )

        return self.__parent__._cast(_4671.RingPinsParametricStudyTool)

    @property
    def rolling_ring_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4673.RollingRingAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4673,
        )

        return self.__parent__._cast(_4673.RollingRingAssemblyParametricStudyTool)

    @property
    def rolling_ring_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4675.RollingRingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4675,
        )

        return self.__parent__._cast(_4675.RollingRingParametricStudyTool)

    @property
    def root_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4676.RootAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4676,
        )

        return self.__parent__._cast(_4676.RootAssemblyParametricStudyTool)

    @property
    def shaft_hub_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4677.ShaftHubConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4677,
        )

        return self.__parent__._cast(_4677.ShaftHubConnectionParametricStudyTool)

    @property
    def shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4678.ShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4678,
        )

        return self.__parent__._cast(_4678.ShaftParametricStudyTool)

    @property
    def specialised_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4680.SpecialisedAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4680,
        )

        return self.__parent__._cast(_4680.SpecialisedAssemblyParametricStudyTool)

    @property
    def spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4682.SpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4682,
        )

        return self.__parent__._cast(_4682.SpiralBevelGearParametricStudyTool)

    @property
    def spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4683.SpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4683,
        )

        return self.__parent__._cast(_4683.SpiralBevelGearSetParametricStudyTool)

    @property
    def spring_damper_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4685.SpringDamperHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4685,
        )

        return self.__parent__._cast(_4685.SpringDamperHalfParametricStudyTool)

    @property
    def spring_damper_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4686.SpringDamperParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4686,
        )

        return self.__parent__._cast(_4686.SpringDamperParametricStudyTool)

    @property
    def straight_bevel_diff_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4688.StraightBevelDiffGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4688,
        )

        return self.__parent__._cast(_4688.StraightBevelDiffGearParametricStudyTool)

    @property
    def straight_bevel_diff_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4689.StraightBevelDiffGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4689,
        )

        return self.__parent__._cast(_4689.StraightBevelDiffGearSetParametricStudyTool)

    @property
    def straight_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4691.StraightBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4691,
        )

        return self.__parent__._cast(_4691.StraightBevelGearParametricStudyTool)

    @property
    def straight_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4692.StraightBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4692,
        )

        return self.__parent__._cast(_4692.StraightBevelGearSetParametricStudyTool)

    @property
    def straight_bevel_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4693.StraightBevelPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4693,
        )

        return self.__parent__._cast(_4693.StraightBevelPlanetGearParametricStudyTool)

    @property
    def straight_bevel_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4694.StraightBevelSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4694,
        )

        return self.__parent__._cast(_4694.StraightBevelSunGearParametricStudyTool)

    @property
    def synchroniser_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4695.SynchroniserHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4695,
        )

        return self.__parent__._cast(_4695.SynchroniserHalfParametricStudyTool)

    @property
    def synchroniser_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4696.SynchroniserParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4696,
        )

        return self.__parent__._cast(_4696.SynchroniserParametricStudyTool)

    @property
    def synchroniser_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4697.SynchroniserPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4697,
        )

        return self.__parent__._cast(_4697.SynchroniserPartParametricStudyTool)

    @property
    def synchroniser_sleeve_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4698.SynchroniserSleeveParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4698,
        )

        return self.__parent__._cast(_4698.SynchroniserSleeveParametricStudyTool)

    @property
    def torque_converter_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4700.TorqueConverterParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4700,
        )

        return self.__parent__._cast(_4700.TorqueConverterParametricStudyTool)

    @property
    def torque_converter_pump_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4701.TorqueConverterPumpParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4701,
        )

        return self.__parent__._cast(_4701.TorqueConverterPumpParametricStudyTool)

    @property
    def torque_converter_turbine_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4702.TorqueConverterTurbineParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4702,
        )

        return self.__parent__._cast(_4702.TorqueConverterTurbineParametricStudyTool)

    @property
    def unbalanced_mass_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4703.UnbalancedMassParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4703,
        )

        return self.__parent__._cast(_4703.UnbalancedMassParametricStudyTool)

    @property
    def virtual_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4704.VirtualComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4704,
        )

        return self.__parent__._cast(_4704.VirtualComponentParametricStudyTool)

    @property
    def worm_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4706.WormGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4706,
        )

        return self.__parent__._cast(_4706.WormGearParametricStudyTool)

    @property
    def worm_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4707.WormGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4707,
        )

        return self.__parent__._cast(_4707.WormGearSetParametricStudyTool)

    @property
    def zerol_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4709.ZerolBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4709,
        )

        return self.__parent__._cast(_4709.ZerolBevelGearParametricStudyTool)

    @property
    def zerol_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4710.ZerolBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4710,
        )

        return self.__parent__._cast(_4710.ZerolBevelGearSetParametricStudyTool)

    @property
    def abstract_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4842.AbstractAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4842,
        )

        return self.__parent__._cast(_4842.AbstractAssemblyModalAnalysis)

    @property
    def abstract_shaft_modal_analysis(
        self: "CastSelf",
    ) -> "_4843.AbstractShaftModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4843,
        )

        return self.__parent__._cast(_4843.AbstractShaftModalAnalysis)

    @property
    def abstract_shaft_or_housing_modal_analysis(
        self: "CastSelf",
    ) -> "_4844.AbstractShaftOrHousingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4844,
        )

        return self.__parent__._cast(_4844.AbstractShaftOrHousingModalAnalysis)

    @property
    def agma_gleason_conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4847.AGMAGleasonConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4847,
        )

        return self.__parent__._cast(_4847.AGMAGleasonConicalGearModalAnalysis)

    @property
    def agma_gleason_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4848.AGMAGleasonConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4848,
        )

        return self.__parent__._cast(_4848.AGMAGleasonConicalGearSetModalAnalysis)

    @property
    def assembly_modal_analysis(self: "CastSelf") -> "_4849.AssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4849,
        )

        return self.__parent__._cast(_4849.AssemblyModalAnalysis)

    @property
    def bearing_modal_analysis(self: "CastSelf") -> "_4850.BearingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4850,
        )

        return self.__parent__._cast(_4850.BearingModalAnalysis)

    @property
    def belt_drive_modal_analysis(self: "CastSelf") -> "_4852.BeltDriveModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4852,
        )

        return self.__parent__._cast(_4852.BeltDriveModalAnalysis)

    @property
    def bevel_differential_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4854.BevelDifferentialGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4854,
        )

        return self.__parent__._cast(_4854.BevelDifferentialGearModalAnalysis)

    @property
    def bevel_differential_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4855.BevelDifferentialGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4855,
        )

        return self.__parent__._cast(_4855.BevelDifferentialGearSetModalAnalysis)

    @property
    def bevel_differential_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4856.BevelDifferentialPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4856,
        )

        return self.__parent__._cast(_4856.BevelDifferentialPlanetGearModalAnalysis)

    @property
    def bevel_differential_sun_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4857.BevelDifferentialSunGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4857,
        )

        return self.__parent__._cast(_4857.BevelDifferentialSunGearModalAnalysis)

    @property
    def bevel_gear_modal_analysis(self: "CastSelf") -> "_4859.BevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4859,
        )

        return self.__parent__._cast(_4859.BevelGearModalAnalysis)

    @property
    def bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4860.BevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4860,
        )

        return self.__parent__._cast(_4860.BevelGearSetModalAnalysis)

    @property
    def bolted_joint_modal_analysis(
        self: "CastSelf",
    ) -> "_4861.BoltedJointModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4861,
        )

        return self.__parent__._cast(_4861.BoltedJointModalAnalysis)

    @property
    def bolt_modal_analysis(self: "CastSelf") -> "_4862.BoltModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4862,
        )

        return self.__parent__._cast(_4862.BoltModalAnalysis)

    @property
    def clutch_half_modal_analysis(self: "CastSelf") -> "_4864.ClutchHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4864,
        )

        return self.__parent__._cast(_4864.ClutchHalfModalAnalysis)

    @property
    def clutch_modal_analysis(self: "CastSelf") -> "_4865.ClutchModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4865,
        )

        return self.__parent__._cast(_4865.ClutchModalAnalysis)

    @property
    def component_modal_analysis(self: "CastSelf") -> "_4867.ComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4867,
        )

        return self.__parent__._cast(_4867.ComponentModalAnalysis)

    @property
    def concept_coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4869.ConceptCouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4869,
        )

        return self.__parent__._cast(_4869.ConceptCouplingHalfModalAnalysis)

    @property
    def concept_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4870.ConceptCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4870,
        )

        return self.__parent__._cast(_4870.ConceptCouplingModalAnalysis)

    @property
    def concept_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4872.ConceptGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4872,
        )

        return self.__parent__._cast(_4872.ConceptGearModalAnalysis)

    @property
    def concept_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4873.ConceptGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4873,
        )

        return self.__parent__._cast(_4873.ConceptGearSetModalAnalysis)

    @property
    def conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4875.ConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4875,
        )

        return self.__parent__._cast(_4875.ConicalGearModalAnalysis)

    @property
    def conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4876.ConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4876,
        )

        return self.__parent__._cast(_4876.ConicalGearSetModalAnalysis)

    @property
    def connector_modal_analysis(self: "CastSelf") -> "_4878.ConnectorModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4878,
        )

        return self.__parent__._cast(_4878.ConnectorModalAnalysis)

    @property
    def coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4881.CouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4881,
        )

        return self.__parent__._cast(_4881.CouplingHalfModalAnalysis)

    @property
    def coupling_modal_analysis(self: "CastSelf") -> "_4882.CouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4882,
        )

        return self.__parent__._cast(_4882.CouplingModalAnalysis)

    @property
    def cvt_modal_analysis(self: "CastSelf") -> "_4884.CVTModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4884,
        )

        return self.__parent__._cast(_4884.CVTModalAnalysis)

    @property
    def cvt_pulley_modal_analysis(self: "CastSelf") -> "_4885.CVTPulleyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4885,
        )

        return self.__parent__._cast(_4885.CVTPulleyModalAnalysis)

    @property
    def cycloidal_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4886.CycloidalAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4886,
        )

        return self.__parent__._cast(_4886.CycloidalAssemblyModalAnalysis)

    @property
    def cycloidal_disc_modal_analysis(
        self: "CastSelf",
    ) -> "_4888.CycloidalDiscModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4888,
        )

        return self.__parent__._cast(_4888.CycloidalDiscModalAnalysis)

    @property
    def cylindrical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4891.CylindricalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4891,
        )

        return self.__parent__._cast(_4891.CylindricalGearModalAnalysis)

    @property
    def cylindrical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4892.CylindricalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4892,
        )

        return self.__parent__._cast(_4892.CylindricalGearSetModalAnalysis)

    @property
    def cylindrical_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4893.CylindricalPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4893,
        )

        return self.__parent__._cast(_4893.CylindricalPlanetGearModalAnalysis)

    @property
    def datum_modal_analysis(self: "CastSelf") -> "_4894.DatumModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4894,
        )

        return self.__parent__._cast(_4894.DatumModalAnalysis)

    @property
    def external_cad_model_modal_analysis(
        self: "CastSelf",
    ) -> "_4898.ExternalCADModelModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4898,
        )

        return self.__parent__._cast(_4898.ExternalCADModelModalAnalysis)

    @property
    def face_gear_modal_analysis(self: "CastSelf") -> "_4900.FaceGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4900,
        )

        return self.__parent__._cast(_4900.FaceGearModalAnalysis)

    @property
    def face_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4901.FaceGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4901,
        )

        return self.__parent__._cast(_4901.FaceGearSetModalAnalysis)

    @property
    def fe_part_modal_analysis(self: "CastSelf") -> "_4902.FEPartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4902,
        )

        return self.__parent__._cast(_4902.FEPartModalAnalysis)

    @property
    def flexible_pin_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4903.FlexiblePinAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4903,
        )

        return self.__parent__._cast(_4903.FlexiblePinAssemblyModalAnalysis)

    @property
    def gear_modal_analysis(self: "CastSelf") -> "_4906.GearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4906,
        )

        return self.__parent__._cast(_4906.GearModalAnalysis)

    @property
    def gear_set_modal_analysis(self: "CastSelf") -> "_4907.GearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4907,
        )

        return self.__parent__._cast(_4907.GearSetModalAnalysis)

    @property
    def guide_dxf_model_modal_analysis(
        self: "CastSelf",
    ) -> "_4908.GuideDxfModelModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4908,
        )

        return self.__parent__._cast(_4908.GuideDxfModelModalAnalysis)

    @property
    def hypoid_gear_modal_analysis(self: "CastSelf") -> "_4910.HypoidGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4910,
        )

        return self.__parent__._cast(_4910.HypoidGearModalAnalysis)

    @property
    def hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4911.HypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4911,
        )

        return self.__parent__._cast(_4911.HypoidGearSetModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4914.KlingelnbergCycloPalloidConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4914,
        )

        return self.__parent__._cast(
            _4914.KlingelnbergCycloPalloidConicalGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4915.KlingelnbergCycloPalloidConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4915,
        )

        return self.__parent__._cast(
            _4915.KlingelnbergCycloPalloidConicalGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4917.KlingelnbergCycloPalloidHypoidGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4917,
        )

        return self.__parent__._cast(
            _4917.KlingelnbergCycloPalloidHypoidGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4918.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4918,
        )

        return self.__parent__._cast(
            _4918.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4920.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4920,
        )

        return self.__parent__._cast(
            _4920.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4921.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4921,
        )

        return self.__parent__._cast(
            _4921.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis
        )

    @property
    def mass_disc_modal_analysis(self: "CastSelf") -> "_4922.MassDiscModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4922,
        )

        return self.__parent__._cast(_4922.MassDiscModalAnalysis)

    @property
    def measurement_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4923.MeasurementComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4923,
        )

        return self.__parent__._cast(_4923.MeasurementComponentModalAnalysis)

    @property
    def microphone_array_modal_analysis(
        self: "CastSelf",
    ) -> "_4924.MicrophoneArrayModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4924,
        )

        return self.__parent__._cast(_4924.MicrophoneArrayModalAnalysis)

    @property
    def microphone_modal_analysis(self: "CastSelf") -> "_4925.MicrophoneModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4925,
        )

        return self.__parent__._cast(_4925.MicrophoneModalAnalysis)

    @property
    def mountable_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4931.MountableComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4931,
        )

        return self.__parent__._cast(_4931.MountableComponentModalAnalysis)

    @property
    def oil_seal_modal_analysis(self: "CastSelf") -> "_4933.OilSealModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4933,
        )

        return self.__parent__._cast(_4933.OilSealModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4935.PartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4935,
        )

        return self.__parent__._cast(_4935.PartModalAnalysis)

    @property
    def part_to_part_shear_coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4937.PartToPartShearCouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4937,
        )

        return self.__parent__._cast(_4937.PartToPartShearCouplingHalfModalAnalysis)

    @property
    def part_to_part_shear_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4938.PartToPartShearCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4938,
        )

        return self.__parent__._cast(_4938.PartToPartShearCouplingModalAnalysis)

    @property
    def planetary_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4940.PlanetaryGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4940,
        )

        return self.__parent__._cast(_4940.PlanetaryGearSetModalAnalysis)

    @property
    def planet_carrier_modal_analysis(
        self: "CastSelf",
    ) -> "_4941.PlanetCarrierModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4941,
        )

        return self.__parent__._cast(_4941.PlanetCarrierModalAnalysis)

    @property
    def point_load_modal_analysis(self: "CastSelf") -> "_4942.PointLoadModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4942,
        )

        return self.__parent__._cast(_4942.PointLoadModalAnalysis)

    @property
    def power_load_modal_analysis(self: "CastSelf") -> "_4943.PowerLoadModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4943,
        )

        return self.__parent__._cast(_4943.PowerLoadModalAnalysis)

    @property
    def pulley_modal_analysis(self: "CastSelf") -> "_4944.PulleyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4944,
        )

        return self.__parent__._cast(_4944.PulleyModalAnalysis)

    @property
    def ring_pins_modal_analysis(self: "CastSelf") -> "_4945.RingPinsModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4945,
        )

        return self.__parent__._cast(_4945.RingPinsModalAnalysis)

    @property
    def rolling_ring_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4947.RollingRingAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4947,
        )

        return self.__parent__._cast(_4947.RollingRingAssemblyModalAnalysis)

    @property
    def rolling_ring_modal_analysis(
        self: "CastSelf",
    ) -> "_4949.RollingRingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4949,
        )

        return self.__parent__._cast(_4949.RollingRingModalAnalysis)

    @property
    def root_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4950.RootAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4950,
        )

        return self.__parent__._cast(_4950.RootAssemblyModalAnalysis)

    @property
    def shaft_hub_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4951.ShaftHubConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4951,
        )

        return self.__parent__._cast(_4951.ShaftHubConnectionModalAnalysis)

    @property
    def shaft_modal_analysis(self: "CastSelf") -> "_4952.ShaftModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4952,
        )

        return self.__parent__._cast(_4952.ShaftModalAnalysis)

    @property
    def specialised_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4955.SpecialisedAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4955,
        )

        return self.__parent__._cast(_4955.SpecialisedAssemblyModalAnalysis)

    @property
    def spiral_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4957.SpiralBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4957,
        )

        return self.__parent__._cast(_4957.SpiralBevelGearModalAnalysis)

    @property
    def spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4958.SpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4958,
        )

        return self.__parent__._cast(_4958.SpiralBevelGearSetModalAnalysis)

    @property
    def spring_damper_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4960.SpringDamperHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4960,
        )

        return self.__parent__._cast(_4960.SpringDamperHalfModalAnalysis)

    @property
    def spring_damper_modal_analysis(
        self: "CastSelf",
    ) -> "_4961.SpringDamperModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4961,
        )

        return self.__parent__._cast(_4961.SpringDamperModalAnalysis)

    @property
    def straight_bevel_diff_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4963.StraightBevelDiffGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4963,
        )

        return self.__parent__._cast(_4963.StraightBevelDiffGearModalAnalysis)

    @property
    def straight_bevel_diff_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4964.StraightBevelDiffGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4964,
        )

        return self.__parent__._cast(_4964.StraightBevelDiffGearSetModalAnalysis)

    @property
    def straight_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4966.StraightBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4966,
        )

        return self.__parent__._cast(_4966.StraightBevelGearModalAnalysis)

    @property
    def straight_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4967.StraightBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4967,
        )

        return self.__parent__._cast(_4967.StraightBevelGearSetModalAnalysis)

    @property
    def straight_bevel_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4968.StraightBevelPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4968,
        )

        return self.__parent__._cast(_4968.StraightBevelPlanetGearModalAnalysis)

    @property
    def straight_bevel_sun_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4969.StraightBevelSunGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4969,
        )

        return self.__parent__._cast(_4969.StraightBevelSunGearModalAnalysis)

    @property
    def synchroniser_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4970.SynchroniserHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4970,
        )

        return self.__parent__._cast(_4970.SynchroniserHalfModalAnalysis)

    @property
    def synchroniser_modal_analysis(
        self: "CastSelf",
    ) -> "_4971.SynchroniserModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4971,
        )

        return self.__parent__._cast(_4971.SynchroniserModalAnalysis)

    @property
    def synchroniser_part_modal_analysis(
        self: "CastSelf",
    ) -> "_4972.SynchroniserPartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4972,
        )

        return self.__parent__._cast(_4972.SynchroniserPartModalAnalysis)

    @property
    def synchroniser_sleeve_modal_analysis(
        self: "CastSelf",
    ) -> "_4973.SynchroniserSleeveModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4973,
        )

        return self.__parent__._cast(_4973.SynchroniserSleeveModalAnalysis)

    @property
    def torque_converter_modal_analysis(
        self: "CastSelf",
    ) -> "_4975.TorqueConverterModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4975,
        )

        return self.__parent__._cast(_4975.TorqueConverterModalAnalysis)

    @property
    def torque_converter_pump_modal_analysis(
        self: "CastSelf",
    ) -> "_4976.TorqueConverterPumpModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4976,
        )

        return self.__parent__._cast(_4976.TorqueConverterPumpModalAnalysis)

    @property
    def torque_converter_turbine_modal_analysis(
        self: "CastSelf",
    ) -> "_4977.TorqueConverterTurbineModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4977,
        )

        return self.__parent__._cast(_4977.TorqueConverterTurbineModalAnalysis)

    @property
    def unbalanced_mass_modal_analysis(
        self: "CastSelf",
    ) -> "_4978.UnbalancedMassModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4978,
        )

        return self.__parent__._cast(_4978.UnbalancedMassModalAnalysis)

    @property
    def virtual_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4979.VirtualComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4979,
        )

        return self.__parent__._cast(_4979.VirtualComponentModalAnalysis)

    @property
    def worm_gear_modal_analysis(self: "CastSelf") -> "_4984.WormGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4984,
        )

        return self.__parent__._cast(_4984.WormGearModalAnalysis)

    @property
    def worm_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4985.WormGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4985,
        )

        return self.__parent__._cast(_4985.WormGearSetModalAnalysis)

    @property
    def zerol_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4987.ZerolBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4987,
        )

        return self.__parent__._cast(_4987.ZerolBevelGearModalAnalysis)

    @property
    def zerol_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4988.ZerolBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4988,
        )

        return self.__parent__._cast(_4988.ZerolBevelGearSetModalAnalysis)

    @property
    def abstract_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5132.AbstractAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5132,
        )

        return self.__parent__._cast(_5132.AbstractAssemblyModalAnalysisAtAStiffness)

    @property
    def abstract_shaft_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5133.AbstractShaftModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5133,
        )

        return self.__parent__._cast(_5133.AbstractShaftModalAnalysisAtAStiffness)

    @property
    def abstract_shaft_or_housing_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5134.AbstractShaftOrHousingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5134,
        )

        return self.__parent__._cast(
            _5134.AbstractShaftOrHousingModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5137.AGMAGleasonConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5137,
        )

        return self.__parent__._cast(
            _5137.AGMAGleasonConicalGearModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5138.AGMAGleasonConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5138,
        )

        return self.__parent__._cast(
            _5138.AGMAGleasonConicalGearSetModalAnalysisAtAStiffness
        )

    @property
    def assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5139.AssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5139,
        )

        return self.__parent__._cast(_5139.AssemblyModalAnalysisAtAStiffness)

    @property
    def bearing_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5140.BearingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5140,
        )

        return self.__parent__._cast(_5140.BearingModalAnalysisAtAStiffness)

    @property
    def belt_drive_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5142.BeltDriveModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5142,
        )

        return self.__parent__._cast(_5142.BeltDriveModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5144.BevelDifferentialGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5144,
        )

        return self.__parent__._cast(
            _5144.BevelDifferentialGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5145.BevelDifferentialGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5145,
        )

        return self.__parent__._cast(
            _5145.BevelDifferentialGearSetModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5146.BevelDifferentialPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5146,
        )

        return self.__parent__._cast(
            _5146.BevelDifferentialPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_sun_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5147.BevelDifferentialSunGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5147,
        )

        return self.__parent__._cast(
            _5147.BevelDifferentialSunGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5149.BevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5149,
        )

        return self.__parent__._cast(_5149.BevelGearModalAnalysisAtAStiffness)

    @property
    def bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5150.BevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5150,
        )

        return self.__parent__._cast(_5150.BevelGearSetModalAnalysisAtAStiffness)

    @property
    def bolted_joint_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5151.BoltedJointModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5151,
        )

        return self.__parent__._cast(_5151.BoltedJointModalAnalysisAtAStiffness)

    @property
    def bolt_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5152.BoltModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5152,
        )

        return self.__parent__._cast(_5152.BoltModalAnalysisAtAStiffness)

    @property
    def clutch_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5154.ClutchHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5154,
        )

        return self.__parent__._cast(_5154.ClutchHalfModalAnalysisAtAStiffness)

    @property
    def clutch_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5155.ClutchModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5155,
        )

        return self.__parent__._cast(_5155.ClutchModalAnalysisAtAStiffness)

    @property
    def component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5157.ComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5157,
        )

        return self.__parent__._cast(_5157.ComponentModalAnalysisAtAStiffness)

    @property
    def concept_coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5159.ConceptCouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5159,
        )

        return self.__parent__._cast(_5159.ConceptCouplingHalfModalAnalysisAtAStiffness)

    @property
    def concept_coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5160.ConceptCouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5160,
        )

        return self.__parent__._cast(_5160.ConceptCouplingModalAnalysisAtAStiffness)

    @property
    def concept_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5162.ConceptGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5162,
        )

        return self.__parent__._cast(_5162.ConceptGearModalAnalysisAtAStiffness)

    @property
    def concept_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5163.ConceptGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5163,
        )

        return self.__parent__._cast(_5163.ConceptGearSetModalAnalysisAtAStiffness)

    @property
    def conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5165.ConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5165,
        )

        return self.__parent__._cast(_5165.ConicalGearModalAnalysisAtAStiffness)

    @property
    def conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5166.ConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5166,
        )

        return self.__parent__._cast(_5166.ConicalGearSetModalAnalysisAtAStiffness)

    @property
    def connector_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5168.ConnectorModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5168,
        )

        return self.__parent__._cast(_5168.ConnectorModalAnalysisAtAStiffness)

    @property
    def coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5170.CouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5170,
        )

        return self.__parent__._cast(_5170.CouplingHalfModalAnalysisAtAStiffness)

    @property
    def coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5171.CouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5171,
        )

        return self.__parent__._cast(_5171.CouplingModalAnalysisAtAStiffness)

    @property
    def cvt_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5173.CVTModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5173,
        )

        return self.__parent__._cast(_5173.CVTModalAnalysisAtAStiffness)

    @property
    def cvt_pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5174.CVTPulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5174,
        )

        return self.__parent__._cast(_5174.CVTPulleyModalAnalysisAtAStiffness)

    @property
    def cycloidal_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5175.CycloidalAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5175,
        )

        return self.__parent__._cast(_5175.CycloidalAssemblyModalAnalysisAtAStiffness)

    @property
    def cycloidal_disc_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5177.CycloidalDiscModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5177,
        )

        return self.__parent__._cast(_5177.CycloidalDiscModalAnalysisAtAStiffness)

    @property
    def cylindrical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5180.CylindricalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5180,
        )

        return self.__parent__._cast(_5180.CylindricalGearModalAnalysisAtAStiffness)

    @property
    def cylindrical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5181.CylindricalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5181,
        )

        return self.__parent__._cast(_5181.CylindricalGearSetModalAnalysisAtAStiffness)

    @property
    def cylindrical_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5182.CylindricalPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5182,
        )

        return self.__parent__._cast(
            _5182.CylindricalPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def datum_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5183.DatumModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5183,
        )

        return self.__parent__._cast(_5183.DatumModalAnalysisAtAStiffness)

    @property
    def external_cad_model_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5185.ExternalCADModelModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5185,
        )

        return self.__parent__._cast(_5185.ExternalCADModelModalAnalysisAtAStiffness)

    @property
    def face_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5187.FaceGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5187,
        )

        return self.__parent__._cast(_5187.FaceGearModalAnalysisAtAStiffness)

    @property
    def face_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5188.FaceGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5188,
        )

        return self.__parent__._cast(_5188.FaceGearSetModalAnalysisAtAStiffness)

    @property
    def fe_part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5189.FEPartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5189,
        )

        return self.__parent__._cast(_5189.FEPartModalAnalysisAtAStiffness)

    @property
    def flexible_pin_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5190.FlexiblePinAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5190,
        )

        return self.__parent__._cast(_5190.FlexiblePinAssemblyModalAnalysisAtAStiffness)

    @property
    def gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5192.GearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5192,
        )

        return self.__parent__._cast(_5192.GearModalAnalysisAtAStiffness)

    @property
    def gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5193.GearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5193,
        )

        return self.__parent__._cast(_5193.GearSetModalAnalysisAtAStiffness)

    @property
    def guide_dxf_model_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5194.GuideDxfModelModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5194,
        )

        return self.__parent__._cast(_5194.GuideDxfModelModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5196.HypoidGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5196,
        )

        return self.__parent__._cast(_5196.HypoidGearModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5197.HypoidGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5197,
        )

        return self.__parent__._cast(_5197.HypoidGearSetModalAnalysisAtAStiffness)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5200.KlingelnbergCycloPalloidConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5200,
        )

        return self.__parent__._cast(
            _5200.KlingelnbergCycloPalloidConicalGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5201.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5201,
        )

        return self.__parent__._cast(
            _5201.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5203.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5203,
        )

        return self.__parent__._cast(
            _5203.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5204.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5204,
        )

        return self.__parent__._cast(
            _5204.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5206.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5206,
        )

        return self.__parent__._cast(
            _5206.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5207.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5207,
        )

        return self.__parent__._cast(
            _5207.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness
        )

    @property
    def mass_disc_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5208.MassDiscModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5208,
        )

        return self.__parent__._cast(_5208.MassDiscModalAnalysisAtAStiffness)

    @property
    def measurement_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5209.MeasurementComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5209,
        )

        return self.__parent__._cast(
            _5209.MeasurementComponentModalAnalysisAtAStiffness
        )

    @property
    def microphone_array_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5210.MicrophoneArrayModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5210,
        )

        return self.__parent__._cast(_5210.MicrophoneArrayModalAnalysisAtAStiffness)

    @property
    def microphone_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5211.MicrophoneModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5211,
        )

        return self.__parent__._cast(_5211.MicrophoneModalAnalysisAtAStiffness)

    @property
    def mountable_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5213.MountableComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5213,
        )

        return self.__parent__._cast(_5213.MountableComponentModalAnalysisAtAStiffness)

    @property
    def oil_seal_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5214.OilSealModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5214,
        )

        return self.__parent__._cast(_5214.OilSealModalAnalysisAtAStiffness)

    @property
    def part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5215.PartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5215,
        )

        return self.__parent__._cast(_5215.PartModalAnalysisAtAStiffness)

    @property
    def part_to_part_shear_coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5217.PartToPartShearCouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5217,
        )

        return self.__parent__._cast(
            _5217.PartToPartShearCouplingHalfModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5218.PartToPartShearCouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5218,
        )

        return self.__parent__._cast(
            _5218.PartToPartShearCouplingModalAnalysisAtAStiffness
        )

    @property
    def planetary_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5220.PlanetaryGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5220,
        )

        return self.__parent__._cast(_5220.PlanetaryGearSetModalAnalysisAtAStiffness)

    @property
    def planet_carrier_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5221.PlanetCarrierModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5221,
        )

        return self.__parent__._cast(_5221.PlanetCarrierModalAnalysisAtAStiffness)

    @property
    def point_load_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5222.PointLoadModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5222,
        )

        return self.__parent__._cast(_5222.PointLoadModalAnalysisAtAStiffness)

    @property
    def power_load_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5223.PowerLoadModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5223,
        )

        return self.__parent__._cast(_5223.PowerLoadModalAnalysisAtAStiffness)

    @property
    def pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5224.PulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5224,
        )

        return self.__parent__._cast(_5224.PulleyModalAnalysisAtAStiffness)

    @property
    def ring_pins_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5225.RingPinsModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5225,
        )

        return self.__parent__._cast(_5225.RingPinsModalAnalysisAtAStiffness)

    @property
    def rolling_ring_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5227.RollingRingAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5227,
        )

        return self.__parent__._cast(_5227.RollingRingAssemblyModalAnalysisAtAStiffness)

    @property
    def rolling_ring_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5229.RollingRingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5229,
        )

        return self.__parent__._cast(_5229.RollingRingModalAnalysisAtAStiffness)

    @property
    def root_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5230.RootAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5230,
        )

        return self.__parent__._cast(_5230.RootAssemblyModalAnalysisAtAStiffness)

    @property
    def shaft_hub_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5231.ShaftHubConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5231,
        )

        return self.__parent__._cast(_5231.ShaftHubConnectionModalAnalysisAtAStiffness)

    @property
    def shaft_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5232.ShaftModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5232,
        )

        return self.__parent__._cast(_5232.ShaftModalAnalysisAtAStiffness)

    @property
    def specialised_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5234.SpecialisedAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5234,
        )

        return self.__parent__._cast(_5234.SpecialisedAssemblyModalAnalysisAtAStiffness)

    @property
    def spiral_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5236.SpiralBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5236,
        )

        return self.__parent__._cast(_5236.SpiralBevelGearModalAnalysisAtAStiffness)

    @property
    def spiral_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5237.SpiralBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5237,
        )

        return self.__parent__._cast(_5237.SpiralBevelGearSetModalAnalysisAtAStiffness)

    @property
    def spring_damper_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5239.SpringDamperHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5239,
        )

        return self.__parent__._cast(_5239.SpringDamperHalfModalAnalysisAtAStiffness)

    @property
    def spring_damper_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5240.SpringDamperModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5240,
        )

        return self.__parent__._cast(_5240.SpringDamperModalAnalysisAtAStiffness)

    @property
    def straight_bevel_diff_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5242.StraightBevelDiffGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5242,
        )

        return self.__parent__._cast(
            _5242.StraightBevelDiffGearModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5243.StraightBevelDiffGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5243,
        )

        return self.__parent__._cast(
            _5243.StraightBevelDiffGearSetModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5245.StraightBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5245,
        )

        return self.__parent__._cast(_5245.StraightBevelGearModalAnalysisAtAStiffness)

    @property
    def straight_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5246.StraightBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5246,
        )

        return self.__parent__._cast(
            _5246.StraightBevelGearSetModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5247.StraightBevelPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5247,
        )

        return self.__parent__._cast(
            _5247.StraightBevelPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_sun_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5248.StraightBevelSunGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5248,
        )

        return self.__parent__._cast(
            _5248.StraightBevelSunGearModalAnalysisAtAStiffness
        )

    @property
    def synchroniser_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5249.SynchroniserHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5249,
        )

        return self.__parent__._cast(_5249.SynchroniserHalfModalAnalysisAtAStiffness)

    @property
    def synchroniser_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5250.SynchroniserModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5250,
        )

        return self.__parent__._cast(_5250.SynchroniserModalAnalysisAtAStiffness)

    @property
    def synchroniser_part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5251.SynchroniserPartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5251,
        )

        return self.__parent__._cast(_5251.SynchroniserPartModalAnalysisAtAStiffness)

    @property
    def synchroniser_sleeve_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5252.SynchroniserSleeveModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5252,
        )

        return self.__parent__._cast(_5252.SynchroniserSleeveModalAnalysisAtAStiffness)

    @property
    def torque_converter_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5254.TorqueConverterModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5254,
        )

        return self.__parent__._cast(_5254.TorqueConverterModalAnalysisAtAStiffness)

    @property
    def torque_converter_pump_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5255.TorqueConverterPumpModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5255,
        )

        return self.__parent__._cast(_5255.TorqueConverterPumpModalAnalysisAtAStiffness)

    @property
    def torque_converter_turbine_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5256.TorqueConverterTurbineModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5256,
        )

        return self.__parent__._cast(
            _5256.TorqueConverterTurbineModalAnalysisAtAStiffness
        )

    @property
    def unbalanced_mass_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5257.UnbalancedMassModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5257,
        )

        return self.__parent__._cast(_5257.UnbalancedMassModalAnalysisAtAStiffness)

    @property
    def virtual_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5258.VirtualComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5258,
        )

        return self.__parent__._cast(_5258.VirtualComponentModalAnalysisAtAStiffness)

    @property
    def worm_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5260.WormGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5260,
        )

        return self.__parent__._cast(_5260.WormGearModalAnalysisAtAStiffness)

    @property
    def worm_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5261.WormGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5261,
        )

        return self.__parent__._cast(_5261.WormGearSetModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5263.ZerolBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5263,
        )

        return self.__parent__._cast(_5263.ZerolBevelGearModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5264.ZerolBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5264,
        )

        return self.__parent__._cast(_5264.ZerolBevelGearSetModalAnalysisAtAStiffness)

    @property
    def abstract_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5396.AbstractAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5396,
        )

        return self.__parent__._cast(_5396.AbstractAssemblyModalAnalysisAtASpeed)

    @property
    def abstract_shaft_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5397.AbstractShaftModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5397,
        )

        return self.__parent__._cast(_5397.AbstractShaftModalAnalysisAtASpeed)

    @property
    def abstract_shaft_or_housing_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5398.AbstractShaftOrHousingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5398,
        )

        return self.__parent__._cast(_5398.AbstractShaftOrHousingModalAnalysisAtASpeed)

    @property
    def agma_gleason_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5401.AGMAGleasonConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5401,
        )

        return self.__parent__._cast(_5401.AGMAGleasonConicalGearModalAnalysisAtASpeed)

    @property
    def agma_gleason_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5402.AGMAGleasonConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5402,
        )

        return self.__parent__._cast(
            _5402.AGMAGleasonConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5403.AssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5403,
        )

        return self.__parent__._cast(_5403.AssemblyModalAnalysisAtASpeed)

    @property
    def bearing_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5404.BearingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5404,
        )

        return self.__parent__._cast(_5404.BearingModalAnalysisAtASpeed)

    @property
    def belt_drive_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5406.BeltDriveModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5406,
        )

        return self.__parent__._cast(_5406.BeltDriveModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5408.BevelDifferentialGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5408,
        )

        return self.__parent__._cast(_5408.BevelDifferentialGearModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5409.BevelDifferentialGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5409,
        )

        return self.__parent__._cast(
            _5409.BevelDifferentialGearSetModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5410.BevelDifferentialPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5410,
        )

        return self.__parent__._cast(
            _5410.BevelDifferentialPlanetGearModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_sun_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5411.BevelDifferentialSunGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5411,
        )

        return self.__parent__._cast(
            _5411.BevelDifferentialSunGearModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5413.BevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5413,
        )

        return self.__parent__._cast(_5413.BevelGearModalAnalysisAtASpeed)

    @property
    def bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5414.BevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5414,
        )

        return self.__parent__._cast(_5414.BevelGearSetModalAnalysisAtASpeed)

    @property
    def bolted_joint_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5415.BoltedJointModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5415,
        )

        return self.__parent__._cast(_5415.BoltedJointModalAnalysisAtASpeed)

    @property
    def bolt_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5416.BoltModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5416,
        )

        return self.__parent__._cast(_5416.BoltModalAnalysisAtASpeed)

    @property
    def clutch_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5418.ClutchHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5418,
        )

        return self.__parent__._cast(_5418.ClutchHalfModalAnalysisAtASpeed)

    @property
    def clutch_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5419.ClutchModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5419,
        )

        return self.__parent__._cast(_5419.ClutchModalAnalysisAtASpeed)

    @property
    def component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5421.ComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5421,
        )

        return self.__parent__._cast(_5421.ComponentModalAnalysisAtASpeed)

    @property
    def concept_coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5423.ConceptCouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5423,
        )

        return self.__parent__._cast(_5423.ConceptCouplingHalfModalAnalysisAtASpeed)

    @property
    def concept_coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5424.ConceptCouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5424,
        )

        return self.__parent__._cast(_5424.ConceptCouplingModalAnalysisAtASpeed)

    @property
    def concept_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5426.ConceptGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5426,
        )

        return self.__parent__._cast(_5426.ConceptGearModalAnalysisAtASpeed)

    @property
    def concept_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5427.ConceptGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5427,
        )

        return self.__parent__._cast(_5427.ConceptGearSetModalAnalysisAtASpeed)

    @property
    def conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5429.ConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5429,
        )

        return self.__parent__._cast(_5429.ConicalGearModalAnalysisAtASpeed)

    @property
    def conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5430.ConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5430,
        )

        return self.__parent__._cast(_5430.ConicalGearSetModalAnalysisAtASpeed)

    @property
    def connector_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5432.ConnectorModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5432,
        )

        return self.__parent__._cast(_5432.ConnectorModalAnalysisAtASpeed)

    @property
    def coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5434.CouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5434,
        )

        return self.__parent__._cast(_5434.CouplingHalfModalAnalysisAtASpeed)

    @property
    def coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5435.CouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5435,
        )

        return self.__parent__._cast(_5435.CouplingModalAnalysisAtASpeed)

    @property
    def cvt_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5437.CVTModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5437,
        )

        return self.__parent__._cast(_5437.CVTModalAnalysisAtASpeed)

    @property
    def cvt_pulley_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5438.CVTPulleyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5438,
        )

        return self.__parent__._cast(_5438.CVTPulleyModalAnalysisAtASpeed)

    @property
    def cycloidal_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5439.CycloidalAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5439,
        )

        return self.__parent__._cast(_5439.CycloidalAssemblyModalAnalysisAtASpeed)

    @property
    def cycloidal_disc_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5441.CycloidalDiscModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5441,
        )

        return self.__parent__._cast(_5441.CycloidalDiscModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5444.CylindricalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5444,
        )

        return self.__parent__._cast(_5444.CylindricalGearModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5445.CylindricalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5445,
        )

        return self.__parent__._cast(_5445.CylindricalGearSetModalAnalysisAtASpeed)

    @property
    def cylindrical_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5446.CylindricalPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5446,
        )

        return self.__parent__._cast(_5446.CylindricalPlanetGearModalAnalysisAtASpeed)

    @property
    def datum_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5447.DatumModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5447,
        )

        return self.__parent__._cast(_5447.DatumModalAnalysisAtASpeed)

    @property
    def external_cad_model_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5448.ExternalCADModelModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5448,
        )

        return self.__parent__._cast(_5448.ExternalCADModelModalAnalysisAtASpeed)

    @property
    def face_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5450.FaceGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5450,
        )

        return self.__parent__._cast(_5450.FaceGearModalAnalysisAtASpeed)

    @property
    def face_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5451.FaceGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5451,
        )

        return self.__parent__._cast(_5451.FaceGearSetModalAnalysisAtASpeed)

    @property
    def fe_part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5452.FEPartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5452,
        )

        return self.__parent__._cast(_5452.FEPartModalAnalysisAtASpeed)

    @property
    def flexible_pin_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5453.FlexiblePinAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5453,
        )

        return self.__parent__._cast(_5453.FlexiblePinAssemblyModalAnalysisAtASpeed)

    @property
    def gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5455.GearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5455,
        )

        return self.__parent__._cast(_5455.GearModalAnalysisAtASpeed)

    @property
    def gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5456.GearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5456,
        )

        return self.__parent__._cast(_5456.GearSetModalAnalysisAtASpeed)

    @property
    def guide_dxf_model_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5457.GuideDxfModelModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5457,
        )

        return self.__parent__._cast(_5457.GuideDxfModelModalAnalysisAtASpeed)

    @property
    def hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5459.HypoidGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5459,
        )

        return self.__parent__._cast(_5459.HypoidGearModalAnalysisAtASpeed)

    @property
    def hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5460.HypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5460,
        )

        return self.__parent__._cast(_5460.HypoidGearSetModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5463.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5463,
        )

        return self.__parent__._cast(
            _5463.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5464.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5464,
        )

        return self.__parent__._cast(
            _5464.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5466.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5466,
        )

        return self.__parent__._cast(
            _5466.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5467.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5467,
        )

        return self.__parent__._cast(
            _5467.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5469.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5469,
        )

        return self.__parent__._cast(
            _5469.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5470.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5470,
        )

        return self.__parent__._cast(
            _5470.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed
        )

    @property
    def mass_disc_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5471.MassDiscModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5471,
        )

        return self.__parent__._cast(_5471.MassDiscModalAnalysisAtASpeed)

    @property
    def measurement_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5472.MeasurementComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5472,
        )

        return self.__parent__._cast(_5472.MeasurementComponentModalAnalysisAtASpeed)

    @property
    def microphone_array_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5473.MicrophoneArrayModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5473,
        )

        return self.__parent__._cast(_5473.MicrophoneArrayModalAnalysisAtASpeed)

    @property
    def microphone_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5474.MicrophoneModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5474,
        )

        return self.__parent__._cast(_5474.MicrophoneModalAnalysisAtASpeed)

    @property
    def mountable_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5476.MountableComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5476,
        )

        return self.__parent__._cast(_5476.MountableComponentModalAnalysisAtASpeed)

    @property
    def oil_seal_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5477.OilSealModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5477,
        )

        return self.__parent__._cast(_5477.OilSealModalAnalysisAtASpeed)

    @property
    def part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5478.PartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5478,
        )

        return self.__parent__._cast(_5478.PartModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5480.PartToPartShearCouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5480,
        )

        return self.__parent__._cast(
            _5480.PartToPartShearCouplingHalfModalAnalysisAtASpeed
        )

    @property
    def part_to_part_shear_coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5481.PartToPartShearCouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5481,
        )

        return self.__parent__._cast(_5481.PartToPartShearCouplingModalAnalysisAtASpeed)

    @property
    def planetary_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5483.PlanetaryGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5483,
        )

        return self.__parent__._cast(_5483.PlanetaryGearSetModalAnalysisAtASpeed)

    @property
    def planet_carrier_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5484.PlanetCarrierModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5484,
        )

        return self.__parent__._cast(_5484.PlanetCarrierModalAnalysisAtASpeed)

    @property
    def point_load_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5485.PointLoadModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5485,
        )

        return self.__parent__._cast(_5485.PointLoadModalAnalysisAtASpeed)

    @property
    def power_load_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5486.PowerLoadModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5486,
        )

        return self.__parent__._cast(_5486.PowerLoadModalAnalysisAtASpeed)

    @property
    def pulley_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5487.PulleyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5487,
        )

        return self.__parent__._cast(_5487.PulleyModalAnalysisAtASpeed)

    @property
    def ring_pins_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5488.RingPinsModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5488,
        )

        return self.__parent__._cast(_5488.RingPinsModalAnalysisAtASpeed)

    @property
    def rolling_ring_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5490.RollingRingAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5490,
        )

        return self.__parent__._cast(_5490.RollingRingAssemblyModalAnalysisAtASpeed)

    @property
    def rolling_ring_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5492.RollingRingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5492,
        )

        return self.__parent__._cast(_5492.RollingRingModalAnalysisAtASpeed)

    @property
    def root_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5493.RootAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5493,
        )

        return self.__parent__._cast(_5493.RootAssemblyModalAnalysisAtASpeed)

    @property
    def shaft_hub_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5494.ShaftHubConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5494,
        )

        return self.__parent__._cast(_5494.ShaftHubConnectionModalAnalysisAtASpeed)

    @property
    def shaft_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5495.ShaftModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5495,
        )

        return self.__parent__._cast(_5495.ShaftModalAnalysisAtASpeed)

    @property
    def specialised_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5497.SpecialisedAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5497,
        )

        return self.__parent__._cast(_5497.SpecialisedAssemblyModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5499.SpiralBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5499,
        )

        return self.__parent__._cast(_5499.SpiralBevelGearModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5500.SpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5500,
        )

        return self.__parent__._cast(_5500.SpiralBevelGearSetModalAnalysisAtASpeed)

    @property
    def spring_damper_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5502.SpringDamperHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5502,
        )

        return self.__parent__._cast(_5502.SpringDamperHalfModalAnalysisAtASpeed)

    @property
    def spring_damper_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5503.SpringDamperModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5503,
        )

        return self.__parent__._cast(_5503.SpringDamperModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5505.StraightBevelDiffGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5505,
        )

        return self.__parent__._cast(_5505.StraightBevelDiffGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5506.StraightBevelDiffGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5506,
        )

        return self.__parent__._cast(
            _5506.StraightBevelDiffGearSetModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5508.StraightBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5508,
        )

        return self.__parent__._cast(_5508.StraightBevelGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5509.StraightBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5509,
        )

        return self.__parent__._cast(_5509.StraightBevelGearSetModalAnalysisAtASpeed)

    @property
    def straight_bevel_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5510.StraightBevelPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5510,
        )

        return self.__parent__._cast(_5510.StraightBevelPlanetGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_sun_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5511.StraightBevelSunGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5511,
        )

        return self.__parent__._cast(_5511.StraightBevelSunGearModalAnalysisAtASpeed)

    @property
    def synchroniser_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5512.SynchroniserHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5512,
        )

        return self.__parent__._cast(_5512.SynchroniserHalfModalAnalysisAtASpeed)

    @property
    def synchroniser_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5513.SynchroniserModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5513,
        )

        return self.__parent__._cast(_5513.SynchroniserModalAnalysisAtASpeed)

    @property
    def synchroniser_part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5514.SynchroniserPartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5514,
        )

        return self.__parent__._cast(_5514.SynchroniserPartModalAnalysisAtASpeed)

    @property
    def synchroniser_sleeve_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5515.SynchroniserSleeveModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5515,
        )

        return self.__parent__._cast(_5515.SynchroniserSleeveModalAnalysisAtASpeed)

    @property
    def torque_converter_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5517.TorqueConverterModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5517,
        )

        return self.__parent__._cast(_5517.TorqueConverterModalAnalysisAtASpeed)

    @property
    def torque_converter_pump_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5518.TorqueConverterPumpModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5518,
        )

        return self.__parent__._cast(_5518.TorqueConverterPumpModalAnalysisAtASpeed)

    @property
    def torque_converter_turbine_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5519.TorqueConverterTurbineModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5519,
        )

        return self.__parent__._cast(_5519.TorqueConverterTurbineModalAnalysisAtASpeed)

    @property
    def unbalanced_mass_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5520.UnbalancedMassModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5520,
        )

        return self.__parent__._cast(_5520.UnbalancedMassModalAnalysisAtASpeed)

    @property
    def virtual_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5521.VirtualComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5521,
        )

        return self.__parent__._cast(_5521.VirtualComponentModalAnalysisAtASpeed)

    @property
    def worm_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5523.WormGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5523,
        )

        return self.__parent__._cast(_5523.WormGearModalAnalysisAtASpeed)

    @property
    def worm_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5524.WormGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5524,
        )

        return self.__parent__._cast(_5524.WormGearSetModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5526.ZerolBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5526,
        )

        return self.__parent__._cast(_5526.ZerolBevelGearModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5527.ZerolBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5527,
        )

        return self.__parent__._cast(_5527.ZerolBevelGearSetModalAnalysisAtASpeed)

    @property
    def abstract_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5659.AbstractAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5659,
        )

        return self.__parent__._cast(_5659.AbstractAssemblyMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5660.AbstractShaftMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5660,
        )

        return self.__parent__._cast(_5660.AbstractShaftMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_or_housing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5661.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5661,
        )

        return self.__parent__._cast(
            _5661.AbstractShaftOrHousingMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5664.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5664,
        )

        return self.__parent__._cast(
            _5664.AGMAGleasonConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5665.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5665,
        )

        return self.__parent__._cast(
            _5665.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis
        )

    @property
    def assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5667.AssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5667,
        )

        return self.__parent__._cast(_5667.AssemblyMultibodyDynamicsAnalysis)

    @property
    def bearing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5669.BearingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5669,
        )

        return self.__parent__._cast(_5669.BearingMultibodyDynamicsAnalysis)

    @property
    def belt_drive_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5672.BeltDriveMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5672,
        )

        return self.__parent__._cast(_5672.BeltDriveMultibodyDynamicsAnalysis)

    @property
    def bevel_differential_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5674.BevelDifferentialGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5674,
        )

        return self.__parent__._cast(
            _5674.BevelDifferentialGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5675.BevelDifferentialGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5675,
        )

        return self.__parent__._cast(
            _5675.BevelDifferentialGearSetMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5676.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5676,
        )

        return self.__parent__._cast(
            _5676.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5677.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5677,
        )

        return self.__parent__._cast(
            _5677.BevelDifferentialSunGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5679.BevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5679,
        )

        return self.__parent__._cast(_5679.BevelGearMultibodyDynamicsAnalysis)

    @property
    def bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5680.BevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5680,
        )

        return self.__parent__._cast(_5680.BevelGearSetMultibodyDynamicsAnalysis)

    @property
    def bolted_joint_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5681.BoltedJointMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5681,
        )

        return self.__parent__._cast(_5681.BoltedJointMultibodyDynamicsAnalysis)

    @property
    def bolt_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5682.BoltMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5682,
        )

        return self.__parent__._cast(_5682.BoltMultibodyDynamicsAnalysis)

    @property
    def clutch_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5684.ClutchHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5684,
        )

        return self.__parent__._cast(_5684.ClutchHalfMultibodyDynamicsAnalysis)

    @property
    def clutch_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5685.ClutchMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5685,
        )

        return self.__parent__._cast(_5685.ClutchMultibodyDynamicsAnalysis)

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5688.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5688,
        )

        return self.__parent__._cast(_5688.ComponentMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5690.ConceptCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5690,
        )

        return self.__parent__._cast(_5690.ConceptCouplingHalfMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5691.ConceptCouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5691,
        )

        return self.__parent__._cast(_5691.ConceptCouplingMultibodyDynamicsAnalysis)

    @property
    def concept_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5693.ConceptGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5693,
        )

        return self.__parent__._cast(_5693.ConceptGearMultibodyDynamicsAnalysis)

    @property
    def concept_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5694.ConceptGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5694,
        )

        return self.__parent__._cast(_5694.ConceptGearSetMultibodyDynamicsAnalysis)

    @property
    def conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5696.ConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5696,
        )

        return self.__parent__._cast(_5696.ConicalGearMultibodyDynamicsAnalysis)

    @property
    def conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5697.ConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5697,
        )

        return self.__parent__._cast(_5697.ConicalGearSetMultibodyDynamicsAnalysis)

    @property
    def connector_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5699.ConnectorMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5699,
        )

        return self.__parent__._cast(_5699.ConnectorMultibodyDynamicsAnalysis)

    @property
    def coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5701.CouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5701,
        )

        return self.__parent__._cast(_5701.CouplingHalfMultibodyDynamicsAnalysis)

    @property
    def coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5702.CouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5702,
        )

        return self.__parent__._cast(_5702.CouplingMultibodyDynamicsAnalysis)

    @property
    def cvt_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5704.CVTMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5704,
        )

        return self.__parent__._cast(_5704.CVTMultibodyDynamicsAnalysis)

    @property
    def cvt_pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5705.CVTPulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5705,
        )

        return self.__parent__._cast(_5705.CVTPulleyMultibodyDynamicsAnalysis)

    @property
    def cycloidal_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5706.CycloidalAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5706,
        )

        return self.__parent__._cast(_5706.CycloidalAssemblyMultibodyDynamicsAnalysis)

    @property
    def cycloidal_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5708.CycloidalDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5708,
        )

        return self.__parent__._cast(_5708.CycloidalDiscMultibodyDynamicsAnalysis)

    @property
    def cylindrical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5711.CylindricalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5711,
        )

        return self.__parent__._cast(_5711.CylindricalGearMultibodyDynamicsAnalysis)

    @property
    def cylindrical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5712.CylindricalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5712,
        )

        return self.__parent__._cast(_5712.CylindricalGearSetMultibodyDynamicsAnalysis)

    @property
    def cylindrical_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5713.CylindricalPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5713,
        )

        return self.__parent__._cast(
            _5713.CylindricalPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def datum_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5714.DatumMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5714,
        )

        return self.__parent__._cast(_5714.DatumMultibodyDynamicsAnalysis)

    @property
    def external_cad_model_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5715.ExternalCADModelMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5715,
        )

        return self.__parent__._cast(_5715.ExternalCADModelMultibodyDynamicsAnalysis)

    @property
    def face_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5717.FaceGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5717,
        )

        return self.__parent__._cast(_5717.FaceGearMultibodyDynamicsAnalysis)

    @property
    def face_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5718.FaceGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5718,
        )

        return self.__parent__._cast(_5718.FaceGearSetMultibodyDynamicsAnalysis)

    @property
    def fe_part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5719.FEPartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5719,
        )

        return self.__parent__._cast(_5719.FEPartMultibodyDynamicsAnalysis)

    @property
    def flexible_pin_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5720.FlexiblePinAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5720,
        )

        return self.__parent__._cast(_5720.FlexiblePinAssemblyMultibodyDynamicsAnalysis)

    @property
    def gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5723.GearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5723,
        )

        return self.__parent__._cast(_5723.GearMultibodyDynamicsAnalysis)

    @property
    def gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5724.GearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5724,
        )

        return self.__parent__._cast(_5724.GearSetMultibodyDynamicsAnalysis)

    @property
    def guide_dxf_model_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5725.GuideDxfModelMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5725,
        )

        return self.__parent__._cast(_5725.GuideDxfModelMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5727.HypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5727,
        )

        return self.__parent__._cast(_5727.HypoidGearMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5728.HypoidGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5728,
        )

        return self.__parent__._cast(_5728.HypoidGearSetMultibodyDynamicsAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5735.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5735,
        )

        return self.__parent__._cast(
            _5735.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5736.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5736,
        )

        return self.__parent__._cast(
            _5736.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5738.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5738,
        )

        return self.__parent__._cast(
            _5738.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5739.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5739,
        )

        return self.__parent__._cast(
            _5739.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5741.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5741,
        )

        return self.__parent__._cast(
            _5741.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5742.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5742,
        )

        return self.__parent__._cast(
            _5742.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis
        )

    @property
    def mass_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5743.MassDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5743,
        )

        return self.__parent__._cast(_5743.MassDiscMultibodyDynamicsAnalysis)

    @property
    def measurement_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5747.MeasurementComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5747,
        )

        return self.__parent__._cast(
            _5747.MeasurementComponentMultibodyDynamicsAnalysis
        )

    @property
    def microphone_array_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5748.MicrophoneArrayMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5748,
        )

        return self.__parent__._cast(_5748.MicrophoneArrayMultibodyDynamicsAnalysis)

    @property
    def microphone_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5749.MicrophoneMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5749,
        )

        return self.__parent__._cast(_5749.MicrophoneMultibodyDynamicsAnalysis)

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5750.MountableComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5750,
        )

        return self.__parent__._cast(_5750.MountableComponentMultibodyDynamicsAnalysis)

    @property
    def oil_seal_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5752.OilSealMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5752,
        )

        return self.__parent__._cast(_5752.OilSealMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5753.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5753,
        )

        return self.__parent__._cast(_5753.PartMultibodyDynamicsAnalysis)

    @property
    def part_to_part_shear_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5755.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5755,
        )

        return self.__parent__._cast(
            _5755.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis
        )

    @property
    def part_to_part_shear_coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5756.PartToPartShearCouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5756,
        )

        return self.__parent__._cast(
            _5756.PartToPartShearCouplingMultibodyDynamicsAnalysis
        )

    @property
    def planetary_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5758.PlanetaryGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5758,
        )

        return self.__parent__._cast(_5758.PlanetaryGearSetMultibodyDynamicsAnalysis)

    @property
    def planet_carrier_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5759.PlanetCarrierMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5759,
        )

        return self.__parent__._cast(_5759.PlanetCarrierMultibodyDynamicsAnalysis)

    @property
    def point_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5760.PointLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5760,
        )

        return self.__parent__._cast(_5760.PointLoadMultibodyDynamicsAnalysis)

    @property
    def power_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5761.PowerLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5761,
        )

        return self.__parent__._cast(_5761.PowerLoadMultibodyDynamicsAnalysis)

    @property
    def pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5762.PulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5762,
        )

        return self.__parent__._cast(_5762.PulleyMultibodyDynamicsAnalysis)

    @property
    def ring_pins_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5763.RingPinsMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5763,
        )

        return self.__parent__._cast(_5763.RingPinsMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5765.RollingRingAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5765,
        )

        return self.__parent__._cast(_5765.RollingRingAssemblyMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5767.RollingRingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5767,
        )

        return self.__parent__._cast(_5767.RollingRingMultibodyDynamicsAnalysis)

    @property
    def root_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5768.RootAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5768,
        )

        return self.__parent__._cast(_5768.RootAssemblyMultibodyDynamicsAnalysis)

    @property
    def shaft_hub_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5771.ShaftHubConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5771,
        )

        return self.__parent__._cast(_5771.ShaftHubConnectionMultibodyDynamicsAnalysis)

    @property
    def shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5772.ShaftMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5772,
        )

        return self.__parent__._cast(_5772.ShaftMultibodyDynamicsAnalysis)

    @property
    def specialised_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5775.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5775,
        )

        return self.__parent__._cast(_5775.SpecialisedAssemblyMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5777.SpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5777,
        )

        return self.__parent__._cast(_5777.SpiralBevelGearMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5778.SpiralBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5778,
        )

        return self.__parent__._cast(_5778.SpiralBevelGearSetMultibodyDynamicsAnalysis)

    @property
    def spring_damper_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5781.SpringDamperHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5781,
        )

        return self.__parent__._cast(_5781.SpringDamperHalfMultibodyDynamicsAnalysis)

    @property
    def spring_damper_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5782.SpringDamperMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5782,
        )

        return self.__parent__._cast(_5782.SpringDamperMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_diff_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5784.StraightBevelDiffGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5784,
        )

        return self.__parent__._cast(
            _5784.StraightBevelDiffGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_diff_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5785.StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5785,
        )

        return self.__parent__._cast(
            _5785.StraightBevelDiffGearSetMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5787.StraightBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5787,
        )

        return self.__parent__._cast(_5787.StraightBevelGearMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5788.StraightBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5788,
        )

        return self.__parent__._cast(
            _5788.StraightBevelGearSetMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5789.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5789,
        )

        return self.__parent__._cast(
            _5789.StraightBevelPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5790.StraightBevelSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5790,
        )

        return self.__parent__._cast(
            _5790.StraightBevelSunGearMultibodyDynamicsAnalysis
        )

    @property
    def synchroniser_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5791.SynchroniserHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5791,
        )

        return self.__parent__._cast(_5791.SynchroniserHalfMultibodyDynamicsAnalysis)

    @property
    def synchroniser_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5792.SynchroniserMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5792,
        )

        return self.__parent__._cast(_5792.SynchroniserMultibodyDynamicsAnalysis)

    @property
    def synchroniser_part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5793.SynchroniserPartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5793,
        )

        return self.__parent__._cast(_5793.SynchroniserPartMultibodyDynamicsAnalysis)

    @property
    def synchroniser_sleeve_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5794.SynchroniserSleeveMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5794,
        )

        return self.__parent__._cast(_5794.SynchroniserSleeveMultibodyDynamicsAnalysis)

    @property
    def torque_converter_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5797.TorqueConverterMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5797,
        )

        return self.__parent__._cast(_5797.TorqueConverterMultibodyDynamicsAnalysis)

    @property
    def torque_converter_pump_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5798.TorqueConverterPumpMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5798,
        )

        return self.__parent__._cast(_5798.TorqueConverterPumpMultibodyDynamicsAnalysis)

    @property
    def torque_converter_turbine_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5800.TorqueConverterTurbineMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5800,
        )

        return self.__parent__._cast(
            _5800.TorqueConverterTurbineMultibodyDynamicsAnalysis
        )

    @property
    def unbalanced_mass_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5801.UnbalancedMassMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5801,
        )

        return self.__parent__._cast(_5801.UnbalancedMassMultibodyDynamicsAnalysis)

    @property
    def virtual_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5802.VirtualComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5802,
        )

        return self.__parent__._cast(_5802.VirtualComponentMultibodyDynamicsAnalysis)

    @property
    def worm_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5805.WormGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5805,
        )

        return self.__parent__._cast(_5805.WormGearMultibodyDynamicsAnalysis)

    @property
    def worm_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5806.WormGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5806,
        )

        return self.__parent__._cast(_5806.WormGearSetMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5808.ZerolBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5808,
        )

        return self.__parent__._cast(_5808.ZerolBevelGearMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5809.ZerolBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5809,
        )

        return self.__parent__._cast(_5809.ZerolBevelGearSetMultibodyDynamicsAnalysis)

    @property
    def abstract_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5968.AbstractAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5968,
        )

        return self.__parent__._cast(_5968.AbstractAssemblyHarmonicAnalysis)

    @property
    def abstract_shaft_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5970.AbstractShaftHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5970,
        )

        return self.__parent__._cast(_5970.AbstractShaftHarmonicAnalysis)

    @property
    def abstract_shaft_or_housing_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5971.AbstractShaftOrHousingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5971,
        )

        return self.__parent__._cast(_5971.AbstractShaftOrHousingHarmonicAnalysis)

    @property
    def agma_gleason_conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5973.AGMAGleasonConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5973,
        )

        return self.__parent__._cast(_5973.AGMAGleasonConicalGearHarmonicAnalysis)

    @property
    def agma_gleason_conical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5975.AGMAGleasonConicalGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5975,
        )

        return self.__parent__._cast(_5975.AGMAGleasonConicalGearSetHarmonicAnalysis)

    @property
    def assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5976.AssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5976,
        )

        return self.__parent__._cast(_5976.AssemblyHarmonicAnalysis)

    @property
    def bearing_harmonic_analysis(self: "CastSelf") -> "_5977.BearingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5977,
        )

        return self.__parent__._cast(_5977.BearingHarmonicAnalysis)

    @property
    def belt_drive_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5979.BeltDriveHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5979,
        )

        return self.__parent__._cast(_5979.BeltDriveHarmonicAnalysis)

    @property
    def bevel_differential_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5980.BevelDifferentialGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5980,
        )

        return self.__parent__._cast(_5980.BevelDifferentialGearHarmonicAnalysis)

    @property
    def bevel_differential_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5982.BevelDifferentialGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5982,
        )

        return self.__parent__._cast(_5982.BevelDifferentialGearSetHarmonicAnalysis)

    @property
    def bevel_differential_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5983.BevelDifferentialPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5983,
        )

        return self.__parent__._cast(_5983.BevelDifferentialPlanetGearHarmonicAnalysis)

    @property
    def bevel_differential_sun_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5984.BevelDifferentialSunGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5984,
        )

        return self.__parent__._cast(_5984.BevelDifferentialSunGearHarmonicAnalysis)

    @property
    def bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5985.BevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5985,
        )

        return self.__parent__._cast(_5985.BevelGearHarmonicAnalysis)

    @property
    def bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5987.BevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5987,
        )

        return self.__parent__._cast(_5987.BevelGearSetHarmonicAnalysis)

    @property
    def bolted_joint_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5988.BoltedJointHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5988,
        )

        return self.__parent__._cast(_5988.BoltedJointHarmonicAnalysis)

    @property
    def bolt_harmonic_analysis(self: "CastSelf") -> "_5989.BoltHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5989,
        )

        return self.__parent__._cast(_5989.BoltHarmonicAnalysis)

    @property
    def clutch_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5991.ClutchHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5991,
        )

        return self.__parent__._cast(_5991.ClutchHalfHarmonicAnalysis)

    @property
    def clutch_harmonic_analysis(self: "CastSelf") -> "_5992.ClutchHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5992,
        )

        return self.__parent__._cast(_5992.ClutchHarmonicAnalysis)

    @property
    def component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5995.ComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5995,
        )

        return self.__parent__._cast(_5995.ComponentHarmonicAnalysis)

    @property
    def concept_coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5997.ConceptCouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5997,
        )

        return self.__parent__._cast(_5997.ConceptCouplingHalfHarmonicAnalysis)

    @property
    def concept_coupling_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5998.ConceptCouplingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5998,
        )

        return self.__parent__._cast(_5998.ConceptCouplingHarmonicAnalysis)

    @property
    def concept_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5999.ConceptGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5999,
        )

        return self.__parent__._cast(_5999.ConceptGearHarmonicAnalysis)

    @property
    def concept_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6001.ConceptGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6001,
        )

        return self.__parent__._cast(_6001.ConceptGearSetHarmonicAnalysis)

    @property
    def conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6002.ConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6002,
        )

        return self.__parent__._cast(_6002.ConicalGearHarmonicAnalysis)

    @property
    def conical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6004.ConicalGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6004,
        )

        return self.__parent__._cast(_6004.ConicalGearSetHarmonicAnalysis)

    @property
    def connector_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6006.ConnectorHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6006,
        )

        return self.__parent__._cast(_6006.ConnectorHarmonicAnalysis)

    @property
    def coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6008.CouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6008,
        )

        return self.__parent__._cast(_6008.CouplingHalfHarmonicAnalysis)

    @property
    def coupling_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6009.CouplingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6009,
        )

        return self.__parent__._cast(_6009.CouplingHarmonicAnalysis)

    @property
    def cvt_harmonic_analysis(self: "CastSelf") -> "_6011.CVTHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6011,
        )

        return self.__parent__._cast(_6011.CVTHarmonicAnalysis)

    @property
    def cvt_pulley_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6012.CVTPulleyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6012,
        )

        return self.__parent__._cast(_6012.CVTPulleyHarmonicAnalysis)

    @property
    def cycloidal_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6013.CycloidalAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6013,
        )

        return self.__parent__._cast(_6013.CycloidalAssemblyHarmonicAnalysis)

    @property
    def cycloidal_disc_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6015.CycloidalDiscHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6015,
        )

        return self.__parent__._cast(_6015.CycloidalDiscHarmonicAnalysis)

    @property
    def cylindrical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6017.CylindricalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6017,
        )

        return self.__parent__._cast(_6017.CylindricalGearHarmonicAnalysis)

    @property
    def cylindrical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6019.CylindricalGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6019,
        )

        return self.__parent__._cast(_6019.CylindricalGearSetHarmonicAnalysis)

    @property
    def cylindrical_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6020.CylindricalPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6020,
        )

        return self.__parent__._cast(_6020.CylindricalPlanetGearHarmonicAnalysis)

    @property
    def datum_harmonic_analysis(self: "CastSelf") -> "_6022.DatumHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6022,
        )

        return self.__parent__._cast(_6022.DatumHarmonicAnalysis)

    @property
    def external_cad_model_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6037.ExternalCADModelHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6037,
        )

        return self.__parent__._cast(_6037.ExternalCADModelHarmonicAnalysis)

    @property
    def face_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6038.FaceGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6038,
        )

        return self.__parent__._cast(_6038.FaceGearHarmonicAnalysis)

    @property
    def face_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6040.FaceGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6040,
        )

        return self.__parent__._cast(_6040.FaceGearSetHarmonicAnalysis)

    @property
    def fe_part_harmonic_analysis(self: "CastSelf") -> "_6041.FEPartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6041,
        )

        return self.__parent__._cast(_6041.FEPartHarmonicAnalysis)

    @property
    def flexible_pin_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6042.FlexiblePinAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6042,
        )

        return self.__parent__._cast(_6042.FlexiblePinAssemblyHarmonicAnalysis)

    @property
    def gear_harmonic_analysis(self: "CastSelf") -> "_6044.GearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6044,
        )

        return self.__parent__._cast(_6044.GearHarmonicAnalysis)

    @property
    def gear_set_harmonic_analysis(self: "CastSelf") -> "_6049.GearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6049,
        )

        return self.__parent__._cast(_6049.GearSetHarmonicAnalysis)

    @property
    def guide_dxf_model_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6051.GuideDxfModelHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6051,
        )

        return self.__parent__._cast(_6051.GuideDxfModelHarmonicAnalysis)

    @property
    def hypoid_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6064.HypoidGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6064,
        )

        return self.__parent__._cast(_6064.HypoidGearHarmonicAnalysis)

    @property
    def hypoid_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6066.HypoidGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6066,
        )

        return self.__parent__._cast(_6066.HypoidGearSetHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6068.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6068,
        )

        return self.__parent__._cast(
            _6068.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6070.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6070,
        )

        return self.__parent__._cast(
            _6070.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6071.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6071,
        )

        return self.__parent__._cast(
            _6071.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6073.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6073,
        )

        return self.__parent__._cast(
            _6073.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6074.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6074,
        )

        return self.__parent__._cast(
            _6074.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6076.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6076,
        )

        return self.__parent__._cast(
            _6076.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis
        )

    @property
    def mass_disc_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6077.MassDiscHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6077,
        )

        return self.__parent__._cast(_6077.MassDiscHarmonicAnalysis)

    @property
    def measurement_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6078.MeasurementComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6078,
        )

        return self.__parent__._cast(_6078.MeasurementComponentHarmonicAnalysis)

    @property
    def microphone_array_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6079.MicrophoneArrayHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6079,
        )

        return self.__parent__._cast(_6079.MicrophoneArrayHarmonicAnalysis)

    @property
    def microphone_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6080.MicrophoneHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6080,
        )

        return self.__parent__._cast(_6080.MicrophoneHarmonicAnalysis)

    @property
    def mountable_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6082.MountableComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6082,
        )

        return self.__parent__._cast(_6082.MountableComponentHarmonicAnalysis)

    @property
    def oil_seal_harmonic_analysis(self: "CastSelf") -> "_6083.OilSealHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6083,
        )

        return self.__parent__._cast(_6083.OilSealHarmonicAnalysis)

    @property
    def part_harmonic_analysis(self: "CastSelf") -> "_6084.PartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6084,
        )

        return self.__parent__._cast(_6084.PartHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6086.PartToPartShearCouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6086,
        )

        return self.__parent__._cast(_6086.PartToPartShearCouplingHalfHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6087.PartToPartShearCouplingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6087,
        )

        return self.__parent__._cast(_6087.PartToPartShearCouplingHarmonicAnalysis)

    @property
    def planetary_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6090.PlanetaryGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6090,
        )

        return self.__parent__._cast(_6090.PlanetaryGearSetHarmonicAnalysis)

    @property
    def planet_carrier_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6091.PlanetCarrierHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6091,
        )

        return self.__parent__._cast(_6091.PlanetCarrierHarmonicAnalysis)

    @property
    def point_load_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6092.PointLoadHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6092,
        )

        return self.__parent__._cast(_6092.PointLoadHarmonicAnalysis)

    @property
    def power_load_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6093.PowerLoadHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6093,
        )

        return self.__parent__._cast(_6093.PowerLoadHarmonicAnalysis)

    @property
    def pulley_harmonic_analysis(self: "CastSelf") -> "_6094.PulleyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6094,
        )

        return self.__parent__._cast(_6094.PulleyHarmonicAnalysis)

    @property
    def ring_pins_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6096.RingPinsHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6096,
        )

        return self.__parent__._cast(_6096.RingPinsHarmonicAnalysis)

    @property
    def rolling_ring_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6098.RollingRingAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6098,
        )

        return self.__parent__._cast(_6098.RollingRingAssemblyHarmonicAnalysis)

    @property
    def rolling_ring_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6100.RollingRingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6100,
        )

        return self.__parent__._cast(_6100.RollingRingHarmonicAnalysis)

    @property
    def root_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6101.RootAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6101,
        )

        return self.__parent__._cast(_6101.RootAssemblyHarmonicAnalysis)

    @property
    def shaft_harmonic_analysis(self: "CastSelf") -> "_6102.ShaftHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6102,
        )

        return self.__parent__._cast(_6102.ShaftHarmonicAnalysis)

    @property
    def shaft_hub_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6103.ShaftHubConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6103,
        )

        return self.__parent__._cast(_6103.ShaftHubConnectionHarmonicAnalysis)

    @property
    def specialised_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6106.SpecialisedAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6106,
        )

        return self.__parent__._cast(_6106.SpecialisedAssemblyHarmonicAnalysis)

    @property
    def spiral_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6108.SpiralBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6108,
        )

        return self.__parent__._cast(_6108.SpiralBevelGearHarmonicAnalysis)

    @property
    def spiral_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6110.SpiralBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6110,
        )

        return self.__parent__._cast(_6110.SpiralBevelGearSetHarmonicAnalysis)

    @property
    def spring_damper_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6112.SpringDamperHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6112,
        )

        return self.__parent__._cast(_6112.SpringDamperHalfHarmonicAnalysis)

    @property
    def spring_damper_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6113.SpringDamperHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6113,
        )

        return self.__parent__._cast(_6113.SpringDamperHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6115.StraightBevelDiffGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6115,
        )

        return self.__parent__._cast(_6115.StraightBevelDiffGearHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6117.StraightBevelDiffGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6117,
        )

        return self.__parent__._cast(_6117.StraightBevelDiffGearSetHarmonicAnalysis)

    @property
    def straight_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6118.StraightBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6118,
        )

        return self.__parent__._cast(_6118.StraightBevelGearHarmonicAnalysis)

    @property
    def straight_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6120.StraightBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6120,
        )

        return self.__parent__._cast(_6120.StraightBevelGearSetHarmonicAnalysis)

    @property
    def straight_bevel_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6121.StraightBevelPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6121,
        )

        return self.__parent__._cast(_6121.StraightBevelPlanetGearHarmonicAnalysis)

    @property
    def straight_bevel_sun_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6122.StraightBevelSunGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6122,
        )

        return self.__parent__._cast(_6122.StraightBevelSunGearHarmonicAnalysis)

    @property
    def synchroniser_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6123.SynchroniserHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6123,
        )

        return self.__parent__._cast(_6123.SynchroniserHalfHarmonicAnalysis)

    @property
    def synchroniser_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6124.SynchroniserHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6124,
        )

        return self.__parent__._cast(_6124.SynchroniserHarmonicAnalysis)

    @property
    def synchroniser_part_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6125.SynchroniserPartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6125,
        )

        return self.__parent__._cast(_6125.SynchroniserPartHarmonicAnalysis)

    @property
    def synchroniser_sleeve_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6126.SynchroniserSleeveHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6126,
        )

        return self.__parent__._cast(_6126.SynchroniserSleeveHarmonicAnalysis)

    @property
    def torque_converter_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6128.TorqueConverterHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6128,
        )

        return self.__parent__._cast(_6128.TorqueConverterHarmonicAnalysis)

    @property
    def torque_converter_pump_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6129.TorqueConverterPumpHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6129,
        )

        return self.__parent__._cast(_6129.TorqueConverterPumpHarmonicAnalysis)

    @property
    def torque_converter_turbine_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6130.TorqueConverterTurbineHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6130,
        )

        return self.__parent__._cast(_6130.TorqueConverterTurbineHarmonicAnalysis)

    @property
    def unbalanced_mass_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6132.UnbalancedMassHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6132,
        )

        return self.__parent__._cast(_6132.UnbalancedMassHarmonicAnalysis)

    @property
    def virtual_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6133.VirtualComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6133,
        )

        return self.__parent__._cast(_6133.VirtualComponentHarmonicAnalysis)

    @property
    def worm_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6134.WormGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6134,
        )

        return self.__parent__._cast(_6134.WormGearHarmonicAnalysis)

    @property
    def worm_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6136.WormGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6136,
        )

        return self.__parent__._cast(_6136.WormGearSetHarmonicAnalysis)

    @property
    def zerol_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6137.ZerolBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6137,
        )

        return self.__parent__._cast(_6137.ZerolBevelGearHarmonicAnalysis)

    @property
    def zerol_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6139.ZerolBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6139,
        )

        return self.__parent__._cast(_6139.ZerolBevelGearSetHarmonicAnalysis)

    @property
    def abstract_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6316.AbstractAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6316,
        )

        return self.__parent__._cast(
            _6316.AbstractAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6317.AbstractShaftHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6317,
        )

        return self.__parent__._cast(
            _6317.AbstractShaftHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_or_housing_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6318.AbstractShaftOrHousingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6318,
        )

        return self.__parent__._cast(
            _6318.AbstractShaftOrHousingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6320.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6320,
        )

        return self.__parent__._cast(
            _6320.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6322.AGMAGleasonConicalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6322,
        )

        return self.__parent__._cast(
            _6322.AGMAGleasonConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6323.AssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6323,
        )

        return self.__parent__._cast(_6323.AssemblyHarmonicAnalysisOfSingleExcitation)

    @property
    def bearing_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6324.BearingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6324,
        )

        return self.__parent__._cast(_6324.BearingHarmonicAnalysisOfSingleExcitation)

    @property
    def belt_drive_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6326.BeltDriveHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6326,
        )

        return self.__parent__._cast(_6326.BeltDriveHarmonicAnalysisOfSingleExcitation)

    @property
    def bevel_differential_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6327.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6327,
        )

        return self.__parent__._cast(
            _6327.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6329.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6329,
        )

        return self.__parent__._cast(
            _6329.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6330.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6330,
        )

        return self.__parent__._cast(
            _6330.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_sun_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6331.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6331,
        )

        return self.__parent__._cast(
            _6331.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6332.BevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6332,
        )

        return self.__parent__._cast(_6332.BevelGearHarmonicAnalysisOfSingleExcitation)

    @property
    def bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6334.BevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6334,
        )

        return self.__parent__._cast(
            _6334.BevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bolted_joint_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6335.BoltedJointHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6335,
        )

        return self.__parent__._cast(
            _6335.BoltedJointHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bolt_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6336.BoltHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6336,
        )

        return self.__parent__._cast(_6336.BoltHarmonicAnalysisOfSingleExcitation)

    @property
    def clutch_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6338.ClutchHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6338,
        )

        return self.__parent__._cast(_6338.ClutchHalfHarmonicAnalysisOfSingleExcitation)

    @property
    def clutch_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6339.ClutchHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6339,
        )

        return self.__parent__._cast(_6339.ClutchHarmonicAnalysisOfSingleExcitation)

    @property
    def component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6341.ComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6341,
        )

        return self.__parent__._cast(_6341.ComponentHarmonicAnalysisOfSingleExcitation)

    @property
    def concept_coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6343.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6343,
        )

        return self.__parent__._cast(
            _6343.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6344.ConceptCouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6344,
        )

        return self.__parent__._cast(
            _6344.ConceptCouplingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6345.ConceptGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6345,
        )

        return self.__parent__._cast(
            _6345.ConceptGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6347.ConceptGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6347,
        )

        return self.__parent__._cast(
            _6347.ConceptGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6348.ConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6348,
        )

        return self.__parent__._cast(
            _6348.ConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6350.ConicalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6350,
        )

        return self.__parent__._cast(
            _6350.ConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connector_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6352.ConnectorHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6352,
        )

        return self.__parent__._cast(_6352.ConnectorHarmonicAnalysisOfSingleExcitation)

    @property
    def coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6354.CouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6354,
        )

        return self.__parent__._cast(
            _6354.CouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6355.CouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6355,
        )

        return self.__parent__._cast(_6355.CouplingHarmonicAnalysisOfSingleExcitation)

    @property
    def cvt_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6357.CVTHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6357,
        )

        return self.__parent__._cast(_6357.CVTHarmonicAnalysisOfSingleExcitation)

    @property
    def cvt_pulley_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6358.CVTPulleyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6358,
        )

        return self.__parent__._cast(_6358.CVTPulleyHarmonicAnalysisOfSingleExcitation)

    @property
    def cycloidal_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6359.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6359,
        )

        return self.__parent__._cast(
            _6359.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6361.CycloidalDiscHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6361,
        )

        return self.__parent__._cast(
            _6361.CycloidalDiscHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6363.CylindricalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6363,
        )

        return self.__parent__._cast(
            _6363.CylindricalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6365.CylindricalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6365,
        )

        return self.__parent__._cast(
            _6365.CylindricalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6366.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6366,
        )

        return self.__parent__._cast(
            _6366.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def datum_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6367.DatumHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6367,
        )

        return self.__parent__._cast(_6367.DatumHarmonicAnalysisOfSingleExcitation)

    @property
    def external_cad_model_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6368.ExternalCADModelHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6368,
        )

        return self.__parent__._cast(
            _6368.ExternalCADModelHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6369.FaceGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6369,
        )

        return self.__parent__._cast(_6369.FaceGearHarmonicAnalysisOfSingleExcitation)

    @property
    def face_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6371.FaceGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6371,
        )

        return self.__parent__._cast(
            _6371.FaceGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def fe_part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6372.FEPartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6372,
        )

        return self.__parent__._cast(_6372.FEPartHarmonicAnalysisOfSingleExcitation)

    @property
    def flexible_pin_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6373.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6373,
        )

        return self.__parent__._cast(
            _6373.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6374.GearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6374,
        )

        return self.__parent__._cast(_6374.GearHarmonicAnalysisOfSingleExcitation)

    @property
    def gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6376.GearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6376,
        )

        return self.__parent__._cast(_6376.GearSetHarmonicAnalysisOfSingleExcitation)

    @property
    def guide_dxf_model_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6377.GuideDxfModelHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6377,
        )

        return self.__parent__._cast(
            _6377.GuideDxfModelHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6379.HypoidGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6379,
        )

        return self.__parent__._cast(_6379.HypoidGearHarmonicAnalysisOfSingleExcitation)

    @property
    def hypoid_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6381.HypoidGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6381,
        )

        return self.__parent__._cast(
            _6381.HypoidGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6383.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6383,
        )

        return self.__parent__._cast(
            _6383.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6385.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6385,
        )

        return self.__parent__._cast(
            _6385.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6386.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6386,
        )

        return self.__parent__._cast(
            _6386.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6388.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6388,
        )

        return self.__parent__._cast(
            _6388.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6389.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6389,
        )

        return self.__parent__._cast(
            _6389.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6391.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6391,
        )

        return self.__parent__._cast(
            _6391.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def mass_disc_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6392.MassDiscHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6392,
        )

        return self.__parent__._cast(_6392.MassDiscHarmonicAnalysisOfSingleExcitation)

    @property
    def measurement_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6393.MeasurementComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6393,
        )

        return self.__parent__._cast(
            _6393.MeasurementComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_array_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6394.MicrophoneArrayHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6394,
        )

        return self.__parent__._cast(
            _6394.MicrophoneArrayHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6395.MicrophoneHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6395,
        )

        return self.__parent__._cast(_6395.MicrophoneHarmonicAnalysisOfSingleExcitation)

    @property
    def mountable_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6397.MountableComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6397,
        )

        return self.__parent__._cast(
            _6397.MountableComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def oil_seal_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6398.OilSealHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6398,
        )

        return self.__parent__._cast(_6398.OilSealHarmonicAnalysisOfSingleExcitation)

    @property
    def part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6399.PartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6399,
        )

        return self.__parent__._cast(_6399.PartHarmonicAnalysisOfSingleExcitation)

    @property
    def part_to_part_shear_coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6401.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6401,
        )

        return self.__parent__._cast(
            _6401.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6402.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6402,
        )

        return self.__parent__._cast(
            _6402.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planetary_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6404.PlanetaryGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6404,
        )

        return self.__parent__._cast(
            _6404.PlanetaryGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planet_carrier_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6405.PlanetCarrierHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6405,
        )

        return self.__parent__._cast(
            _6405.PlanetCarrierHarmonicAnalysisOfSingleExcitation
        )

    @property
    def point_load_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6406.PointLoadHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6406,
        )

        return self.__parent__._cast(_6406.PointLoadHarmonicAnalysisOfSingleExcitation)

    @property
    def power_load_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6407.PowerLoadHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6407,
        )

        return self.__parent__._cast(_6407.PowerLoadHarmonicAnalysisOfSingleExcitation)

    @property
    def pulley_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6408.PulleyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6408,
        )

        return self.__parent__._cast(_6408.PulleyHarmonicAnalysisOfSingleExcitation)

    @property
    def ring_pins_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6409.RingPinsHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6409,
        )

        return self.__parent__._cast(_6409.RingPinsHarmonicAnalysisOfSingleExcitation)

    @property
    def rolling_ring_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6411.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6411,
        )

        return self.__parent__._cast(
            _6411.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6413.RollingRingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6413,
        )

        return self.__parent__._cast(
            _6413.RollingRingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def root_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6414.RootAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6414,
        )

        return self.__parent__._cast(
            _6414.RootAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6415.ShaftHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6415,
        )

        return self.__parent__._cast(_6415.ShaftHarmonicAnalysisOfSingleExcitation)

    @property
    def shaft_hub_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6416.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6416,
        )

        return self.__parent__._cast(
            _6416.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def specialised_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6418.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6418,
        )

        return self.__parent__._cast(
            _6418.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6419.SpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6419,
        )

        return self.__parent__._cast(
            _6419.SpiralBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6421.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6421,
        )

        return self.__parent__._cast(
            _6421.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6423.SpringDamperHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6423,
        )

        return self.__parent__._cast(
            _6423.SpringDamperHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6424.SpringDamperHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6424,
        )

        return self.__parent__._cast(
            _6424.SpringDamperHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6425.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6425,
        )

        return self.__parent__._cast(
            _6425.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6427.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6427,
        )

        return self.__parent__._cast(
            _6427.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6428.StraightBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6428,
        )

        return self.__parent__._cast(
            _6428.StraightBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6430.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6430,
        )

        return self.__parent__._cast(
            _6430.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6431.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6431,
        )

        return self.__parent__._cast(
            _6431.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_sun_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6432.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6432,
        )

        return self.__parent__._cast(
            _6432.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6433.SynchroniserHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6433,
        )

        return self.__parent__._cast(
            _6433.SynchroniserHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6434.SynchroniserHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6434,
        )

        return self.__parent__._cast(
            _6434.SynchroniserHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6435.SynchroniserPartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6435,
        )

        return self.__parent__._cast(
            _6435.SynchroniserPartHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_sleeve_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6436.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6436,
        )

        return self.__parent__._cast(
            _6436.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6438.TorqueConverterHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6438,
        )

        return self.__parent__._cast(
            _6438.TorqueConverterHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_pump_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6439.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6439,
        )

        return self.__parent__._cast(
            _6439.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_turbine_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6440.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6440,
        )

        return self.__parent__._cast(
            _6440.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation
        )

    @property
    def unbalanced_mass_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6441.UnbalancedMassHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6441,
        )

        return self.__parent__._cast(
            _6441.UnbalancedMassHarmonicAnalysisOfSingleExcitation
        )

    @property
    def virtual_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6442.VirtualComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6442,
        )

        return self.__parent__._cast(
            _6442.VirtualComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6443.WormGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6443,
        )

        return self.__parent__._cast(_6443.WormGearHarmonicAnalysisOfSingleExcitation)

    @property
    def worm_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6445.WormGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6445,
        )

        return self.__parent__._cast(
            _6445.WormGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6446.ZerolBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6446,
        )

        return self.__parent__._cast(
            _6446.ZerolBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6448.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6448,
        )

        return self.__parent__._cast(
            _6448.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6589.AbstractAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6589,
        )

        return self.__parent__._cast(_6589.AbstractAssemblyDynamicAnalysis)

    @property
    def abstract_shaft_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6590.AbstractShaftDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6590,
        )

        return self.__parent__._cast(_6590.AbstractShaftDynamicAnalysis)

    @property
    def abstract_shaft_or_housing_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6591.AbstractShaftOrHousingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6591,
        )

        return self.__parent__._cast(_6591.AbstractShaftOrHousingDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6593.AGMAGleasonConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6593,
        )

        return self.__parent__._cast(_6593.AGMAGleasonConicalGearDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6595.AGMAGleasonConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6595,
        )

        return self.__parent__._cast(_6595.AGMAGleasonConicalGearSetDynamicAnalysis)

    @property
    def assembly_dynamic_analysis(self: "CastSelf") -> "_6596.AssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6596,
        )

        return self.__parent__._cast(_6596.AssemblyDynamicAnalysis)

    @property
    def bearing_dynamic_analysis(self: "CastSelf") -> "_6597.BearingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6597,
        )

        return self.__parent__._cast(_6597.BearingDynamicAnalysis)

    @property
    def belt_drive_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6599.BeltDriveDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6599,
        )

        return self.__parent__._cast(_6599.BeltDriveDynamicAnalysis)

    @property
    def bevel_differential_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6600.BevelDifferentialGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6600,
        )

        return self.__parent__._cast(_6600.BevelDifferentialGearDynamicAnalysis)

    @property
    def bevel_differential_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6602.BevelDifferentialGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6602,
        )

        return self.__parent__._cast(_6602.BevelDifferentialGearSetDynamicAnalysis)

    @property
    def bevel_differential_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6603.BevelDifferentialPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6603,
        )

        return self.__parent__._cast(_6603.BevelDifferentialPlanetGearDynamicAnalysis)

    @property
    def bevel_differential_sun_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6604.BevelDifferentialSunGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6604,
        )

        return self.__parent__._cast(_6604.BevelDifferentialSunGearDynamicAnalysis)

    @property
    def bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6605.BevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6605,
        )

        return self.__parent__._cast(_6605.BevelGearDynamicAnalysis)

    @property
    def bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6607.BevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6607,
        )

        return self.__parent__._cast(_6607.BevelGearSetDynamicAnalysis)

    @property
    def bolt_dynamic_analysis(self: "CastSelf") -> "_6608.BoltDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6608,
        )

        return self.__parent__._cast(_6608.BoltDynamicAnalysis)

    @property
    def bolted_joint_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6609.BoltedJointDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6609,
        )

        return self.__parent__._cast(_6609.BoltedJointDynamicAnalysis)

    @property
    def clutch_dynamic_analysis(self: "CastSelf") -> "_6611.ClutchDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6611,
        )

        return self.__parent__._cast(_6611.ClutchDynamicAnalysis)

    @property
    def clutch_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6612.ClutchHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6612,
        )

        return self.__parent__._cast(_6612.ClutchHalfDynamicAnalysis)

    @property
    def component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6614.ComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6614,
        )

        return self.__parent__._cast(_6614.ComponentDynamicAnalysis)

    @property
    def concept_coupling_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6616.ConceptCouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6616,
        )

        return self.__parent__._cast(_6616.ConceptCouplingDynamicAnalysis)

    @property
    def concept_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6617.ConceptCouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6617,
        )

        return self.__parent__._cast(_6617.ConceptCouplingHalfDynamicAnalysis)

    @property
    def concept_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6618.ConceptGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6618,
        )

        return self.__parent__._cast(_6618.ConceptGearDynamicAnalysis)

    @property
    def concept_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6620.ConceptGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6620,
        )

        return self.__parent__._cast(_6620.ConceptGearSetDynamicAnalysis)

    @property
    def conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6621.ConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6621,
        )

        return self.__parent__._cast(_6621.ConicalGearDynamicAnalysis)

    @property
    def conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6623.ConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6623,
        )

        return self.__parent__._cast(_6623.ConicalGearSetDynamicAnalysis)

    @property
    def connector_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6625.ConnectorDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6625,
        )

        return self.__parent__._cast(_6625.ConnectorDynamicAnalysis)

    @property
    def coupling_dynamic_analysis(self: "CastSelf") -> "_6627.CouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6627,
        )

        return self.__parent__._cast(_6627.CouplingDynamicAnalysis)

    @property
    def coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.CouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6628,
        )

        return self.__parent__._cast(_6628.CouplingHalfDynamicAnalysis)

    @property
    def cvt_dynamic_analysis(self: "CastSelf") -> "_6630.CVTDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6630,
        )

        return self.__parent__._cast(_6630.CVTDynamicAnalysis)

    @property
    def cvt_pulley_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6631.CVTPulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6631,
        )

        return self.__parent__._cast(_6631.CVTPulleyDynamicAnalysis)

    @property
    def cycloidal_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6632.CycloidalAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6632,
        )

        return self.__parent__._cast(_6632.CycloidalAssemblyDynamicAnalysis)

    @property
    def cycloidal_disc_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6634.CycloidalDiscDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6634,
        )

        return self.__parent__._cast(_6634.CycloidalDiscDynamicAnalysis)

    @property
    def cylindrical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6636.CylindricalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6636,
        )

        return self.__parent__._cast(_6636.CylindricalGearDynamicAnalysis)

    @property
    def cylindrical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6638.CylindricalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6638,
        )

        return self.__parent__._cast(_6638.CylindricalGearSetDynamicAnalysis)

    @property
    def cylindrical_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6639.CylindricalPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6639,
        )

        return self.__parent__._cast(_6639.CylindricalPlanetGearDynamicAnalysis)

    @property
    def datum_dynamic_analysis(self: "CastSelf") -> "_6640.DatumDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6640,
        )

        return self.__parent__._cast(_6640.DatumDynamicAnalysis)

    @property
    def external_cad_model_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6643.ExternalCADModelDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6643,
        )

        return self.__parent__._cast(_6643.ExternalCADModelDynamicAnalysis)

    @property
    def face_gear_dynamic_analysis(self: "CastSelf") -> "_6644.FaceGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6644,
        )

        return self.__parent__._cast(_6644.FaceGearDynamicAnalysis)

    @property
    def face_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6646.FaceGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6646,
        )

        return self.__parent__._cast(_6646.FaceGearSetDynamicAnalysis)

    @property
    def fe_part_dynamic_analysis(self: "CastSelf") -> "_6647.FEPartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6647,
        )

        return self.__parent__._cast(_6647.FEPartDynamicAnalysis)

    @property
    def flexible_pin_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6648.FlexiblePinAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6648,
        )

        return self.__parent__._cast(_6648.FlexiblePinAssemblyDynamicAnalysis)

    @property
    def gear_dynamic_analysis(self: "CastSelf") -> "_6649.GearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6649,
        )

        return self.__parent__._cast(_6649.GearDynamicAnalysis)

    @property
    def gear_set_dynamic_analysis(self: "CastSelf") -> "_6651.GearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6651,
        )

        return self.__parent__._cast(_6651.GearSetDynamicAnalysis)

    @property
    def guide_dxf_model_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6652.GuideDxfModelDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6652,
        )

        return self.__parent__._cast(_6652.GuideDxfModelDynamicAnalysis)

    @property
    def hypoid_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6653.HypoidGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6653,
        )

        return self.__parent__._cast(_6653.HypoidGearDynamicAnalysis)

    @property
    def hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6655.HypoidGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6655,
        )

        return self.__parent__._cast(_6655.HypoidGearSetDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6657.KlingelnbergCycloPalloidConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6657,
        )

        return self.__parent__._cast(
            _6657.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6659.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6659,
        )

        return self.__parent__._cast(
            _6659.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6660.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6660,
        )

        return self.__parent__._cast(
            _6660.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6662.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6662,
        )

        return self.__parent__._cast(
            _6662.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6663.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6663,
        )

        return self.__parent__._cast(
            _6663.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6665.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6665,
        )

        return self.__parent__._cast(
            _6665.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
        )

    @property
    def mass_disc_dynamic_analysis(self: "CastSelf") -> "_6666.MassDiscDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6666,
        )

        return self.__parent__._cast(_6666.MassDiscDynamicAnalysis)

    @property
    def measurement_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6667.MeasurementComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6667,
        )

        return self.__parent__._cast(_6667.MeasurementComponentDynamicAnalysis)

    @property
    def microphone_array_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6668.MicrophoneArrayDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6668,
        )

        return self.__parent__._cast(_6668.MicrophoneArrayDynamicAnalysis)

    @property
    def microphone_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6669.MicrophoneDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6669,
        )

        return self.__parent__._cast(_6669.MicrophoneDynamicAnalysis)

    @property
    def mountable_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6670.MountableComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6670,
        )

        return self.__parent__._cast(_6670.MountableComponentDynamicAnalysis)

    @property
    def oil_seal_dynamic_analysis(self: "CastSelf") -> "_6671.OilSealDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6671,
        )

        return self.__parent__._cast(_6671.OilSealDynamicAnalysis)

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6672.PartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6672,
        )

        return self.__parent__._cast(_6672.PartDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6674.PartToPartShearCouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6674,
        )

        return self.__parent__._cast(_6674.PartToPartShearCouplingDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6675.PartToPartShearCouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6675,
        )

        return self.__parent__._cast(_6675.PartToPartShearCouplingHalfDynamicAnalysis)

    @property
    def planetary_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6677.PlanetaryGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6677,
        )

        return self.__parent__._cast(_6677.PlanetaryGearSetDynamicAnalysis)

    @property
    def planet_carrier_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6678.PlanetCarrierDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6678,
        )

        return self.__parent__._cast(_6678.PlanetCarrierDynamicAnalysis)

    @property
    def point_load_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6679.PointLoadDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6679,
        )

        return self.__parent__._cast(_6679.PointLoadDynamicAnalysis)

    @property
    def power_load_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6680.PowerLoadDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6680,
        )

        return self.__parent__._cast(_6680.PowerLoadDynamicAnalysis)

    @property
    def pulley_dynamic_analysis(self: "CastSelf") -> "_6681.PulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6681,
        )

        return self.__parent__._cast(_6681.PulleyDynamicAnalysis)

    @property
    def ring_pins_dynamic_analysis(self: "CastSelf") -> "_6682.RingPinsDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6682,
        )

        return self.__parent__._cast(_6682.RingPinsDynamicAnalysis)

    @property
    def rolling_ring_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6684.RollingRingAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6684,
        )

        return self.__parent__._cast(_6684.RollingRingAssemblyDynamicAnalysis)

    @property
    def rolling_ring_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6686.RollingRingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6686,
        )

        return self.__parent__._cast(_6686.RollingRingDynamicAnalysis)

    @property
    def root_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6687.RootAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6687,
        )

        return self.__parent__._cast(_6687.RootAssemblyDynamicAnalysis)

    @property
    def shaft_dynamic_analysis(self: "CastSelf") -> "_6688.ShaftDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6688,
        )

        return self.__parent__._cast(_6688.ShaftDynamicAnalysis)

    @property
    def shaft_hub_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6689.ShaftHubConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6689,
        )

        return self.__parent__._cast(_6689.ShaftHubConnectionDynamicAnalysis)

    @property
    def specialised_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6691.SpecialisedAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6691,
        )

        return self.__parent__._cast(_6691.SpecialisedAssemblyDynamicAnalysis)

    @property
    def spiral_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6692.SpiralBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6692,
        )

        return self.__parent__._cast(_6692.SpiralBevelGearDynamicAnalysis)

    @property
    def spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6694.SpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6694,
        )

        return self.__parent__._cast(_6694.SpiralBevelGearSetDynamicAnalysis)

    @property
    def spring_damper_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6696.SpringDamperDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6696,
        )

        return self.__parent__._cast(_6696.SpringDamperDynamicAnalysis)

    @property
    def spring_damper_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6697.SpringDamperHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6697,
        )

        return self.__parent__._cast(_6697.SpringDamperHalfDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6698.StraightBevelDiffGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6698,
        )

        return self.__parent__._cast(_6698.StraightBevelDiffGearDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6700.StraightBevelDiffGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6700,
        )

        return self.__parent__._cast(_6700.StraightBevelDiffGearSetDynamicAnalysis)

    @property
    def straight_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6701.StraightBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6701,
        )

        return self.__parent__._cast(_6701.StraightBevelGearDynamicAnalysis)

    @property
    def straight_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6703.StraightBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6703,
        )

        return self.__parent__._cast(_6703.StraightBevelGearSetDynamicAnalysis)

    @property
    def straight_bevel_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6704.StraightBevelPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6704,
        )

        return self.__parent__._cast(_6704.StraightBevelPlanetGearDynamicAnalysis)

    @property
    def straight_bevel_sun_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6705.StraightBevelSunGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6705,
        )

        return self.__parent__._cast(_6705.StraightBevelSunGearDynamicAnalysis)

    @property
    def synchroniser_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6706.SynchroniserDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6706,
        )

        return self.__parent__._cast(_6706.SynchroniserDynamicAnalysis)

    @property
    def synchroniser_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6707.SynchroniserHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6707,
        )

        return self.__parent__._cast(_6707.SynchroniserHalfDynamicAnalysis)

    @property
    def synchroniser_part_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6708.SynchroniserPartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6708,
        )

        return self.__parent__._cast(_6708.SynchroniserPartDynamicAnalysis)

    @property
    def synchroniser_sleeve_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6709.SynchroniserSleeveDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6709,
        )

        return self.__parent__._cast(_6709.SynchroniserSleeveDynamicAnalysis)

    @property
    def torque_converter_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6711.TorqueConverterDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6711,
        )

        return self.__parent__._cast(_6711.TorqueConverterDynamicAnalysis)

    @property
    def torque_converter_pump_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6712.TorqueConverterPumpDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6712,
        )

        return self.__parent__._cast(_6712.TorqueConverterPumpDynamicAnalysis)

    @property
    def torque_converter_turbine_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6713.TorqueConverterTurbineDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6713,
        )

        return self.__parent__._cast(_6713.TorqueConverterTurbineDynamicAnalysis)

    @property
    def unbalanced_mass_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6714.UnbalancedMassDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6714,
        )

        return self.__parent__._cast(_6714.UnbalancedMassDynamicAnalysis)

    @property
    def virtual_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6715.VirtualComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6715,
        )

        return self.__parent__._cast(_6715.VirtualComponentDynamicAnalysis)

    @property
    def worm_gear_dynamic_analysis(self: "CastSelf") -> "_6716.WormGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6716,
        )

        return self.__parent__._cast(_6716.WormGearDynamicAnalysis)

    @property
    def worm_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6718.WormGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6718,
        )

        return self.__parent__._cast(_6718.WormGearSetDynamicAnalysis)

    @property
    def zerol_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6719.ZerolBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6719,
        )

        return self.__parent__._cast(_6719.ZerolBevelGearDynamicAnalysis)

    @property
    def zerol_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6721.ZerolBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6721,
        )

        return self.__parent__._cast(_6721.ZerolBevelGearSetDynamicAnalysis)

    @property
    def abstract_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6859.AbstractAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6859,
        )

        return self.__parent__._cast(_6859.AbstractAssemblyCriticalSpeedAnalysis)

    @property
    def abstract_shaft_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6860.AbstractShaftCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6860,
        )

        return self.__parent__._cast(_6860.AbstractShaftCriticalSpeedAnalysis)

    @property
    def abstract_shaft_or_housing_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6861.AbstractShaftOrHousingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6861,
        )

        return self.__parent__._cast(_6861.AbstractShaftOrHousingCriticalSpeedAnalysis)

    @property
    def agma_gleason_conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6863.AGMAGleasonConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6863,
        )

        return self.__parent__._cast(_6863.AGMAGleasonConicalGearCriticalSpeedAnalysis)

    @property
    def agma_gleason_conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6865.AGMAGleasonConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6865,
        )

        return self.__parent__._cast(
            _6865.AGMAGleasonConicalGearSetCriticalSpeedAnalysis
        )

    @property
    def assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6866.AssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6866,
        )

        return self.__parent__._cast(_6866.AssemblyCriticalSpeedAnalysis)

    @property
    def bearing_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6867.BearingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6867,
        )

        return self.__parent__._cast(_6867.BearingCriticalSpeedAnalysis)

    @property
    def belt_drive_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6869.BeltDriveCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6869,
        )

        return self.__parent__._cast(_6869.BeltDriveCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6870.BevelDifferentialGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6870,
        )

        return self.__parent__._cast(_6870.BevelDifferentialGearCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6872.BevelDifferentialGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6872,
        )

        return self.__parent__._cast(
            _6872.BevelDifferentialGearSetCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_planet_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6873.BevelDifferentialPlanetGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6873,
        )

        return self.__parent__._cast(
            _6873.BevelDifferentialPlanetGearCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_sun_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6874.BevelDifferentialSunGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6874,
        )

        return self.__parent__._cast(
            _6874.BevelDifferentialSunGearCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6875.BevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6875,
        )

        return self.__parent__._cast(_6875.BevelGearCriticalSpeedAnalysis)

    @property
    def bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6877.BevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6877,
        )

        return self.__parent__._cast(_6877.BevelGearSetCriticalSpeedAnalysis)

    @property
    def bolt_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6878.BoltCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6878,
        )

        return self.__parent__._cast(_6878.BoltCriticalSpeedAnalysis)

    @property
    def bolted_joint_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6879.BoltedJointCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6879,
        )

        return self.__parent__._cast(_6879.BoltedJointCriticalSpeedAnalysis)

    @property
    def clutch_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6881.ClutchCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6881,
        )

        return self.__parent__._cast(_6881.ClutchCriticalSpeedAnalysis)

    @property
    def clutch_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6882.ClutchHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6882,
        )

        return self.__parent__._cast(_6882.ClutchHalfCriticalSpeedAnalysis)

    @property
    def component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6884.ComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6884,
        )

        return self.__parent__._cast(_6884.ComponentCriticalSpeedAnalysis)

    @property
    def concept_coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6886.ConceptCouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6886,
        )

        return self.__parent__._cast(_6886.ConceptCouplingCriticalSpeedAnalysis)

    @property
    def concept_coupling_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6887.ConceptCouplingHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6887,
        )

        return self.__parent__._cast(_6887.ConceptCouplingHalfCriticalSpeedAnalysis)

    @property
    def concept_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6888.ConceptGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6888,
        )

        return self.__parent__._cast(_6888.ConceptGearCriticalSpeedAnalysis)

    @property
    def concept_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6890.ConceptGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6890,
        )

        return self.__parent__._cast(_6890.ConceptGearSetCriticalSpeedAnalysis)

    @property
    def conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6891.ConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6891,
        )

        return self.__parent__._cast(_6891.ConicalGearCriticalSpeedAnalysis)

    @property
    def conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6893.ConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6893,
        )

        return self.__parent__._cast(_6893.ConicalGearSetCriticalSpeedAnalysis)

    @property
    def connector_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6895.ConnectorCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6895,
        )

        return self.__parent__._cast(_6895.ConnectorCriticalSpeedAnalysis)

    @property
    def coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6897.CouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6897,
        )

        return self.__parent__._cast(_6897.CouplingCriticalSpeedAnalysis)

    @property
    def coupling_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6898.CouplingHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6898,
        )

        return self.__parent__._cast(_6898.CouplingHalfCriticalSpeedAnalysis)

    @property
    def cvt_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6903.CVTCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6903,
        )

        return self.__parent__._cast(_6903.CVTCriticalSpeedAnalysis)

    @property
    def cvt_pulley_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6904.CVTPulleyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6904,
        )

        return self.__parent__._cast(_6904.CVTPulleyCriticalSpeedAnalysis)

    @property
    def cycloidal_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6905.CycloidalAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6905,
        )

        return self.__parent__._cast(_6905.CycloidalAssemblyCriticalSpeedAnalysis)

    @property
    def cycloidal_disc_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6907.CycloidalDiscCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6907,
        )

        return self.__parent__._cast(_6907.CycloidalDiscCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6909.CylindricalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6909,
        )

        return self.__parent__._cast(_6909.CylindricalGearCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6911.CylindricalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6911,
        )

        return self.__parent__._cast(_6911.CylindricalGearSetCriticalSpeedAnalysis)

    @property
    def cylindrical_planet_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6912.CylindricalPlanetGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6912,
        )

        return self.__parent__._cast(_6912.CylindricalPlanetGearCriticalSpeedAnalysis)

    @property
    def datum_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6913.DatumCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6913,
        )

        return self.__parent__._cast(_6913.DatumCriticalSpeedAnalysis)

    @property
    def external_cad_model_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6914.ExternalCADModelCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6914,
        )

        return self.__parent__._cast(_6914.ExternalCADModelCriticalSpeedAnalysis)

    @property
    def face_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6915.FaceGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6915,
        )

        return self.__parent__._cast(_6915.FaceGearCriticalSpeedAnalysis)

    @property
    def face_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6917.FaceGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6917,
        )

        return self.__parent__._cast(_6917.FaceGearSetCriticalSpeedAnalysis)

    @property
    def fe_part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6918.FEPartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6918,
        )

        return self.__parent__._cast(_6918.FEPartCriticalSpeedAnalysis)

    @property
    def flexible_pin_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6919.FlexiblePinAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6919,
        )

        return self.__parent__._cast(_6919.FlexiblePinAssemblyCriticalSpeedAnalysis)

    @property
    def gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6920.GearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6920,
        )

        return self.__parent__._cast(_6920.GearCriticalSpeedAnalysis)

    @property
    def gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6922.GearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6922,
        )

        return self.__parent__._cast(_6922.GearSetCriticalSpeedAnalysis)

    @property
    def guide_dxf_model_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6923.GuideDxfModelCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6923,
        )

        return self.__parent__._cast(_6923.GuideDxfModelCriticalSpeedAnalysis)

    @property
    def hypoid_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6924.HypoidGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6924,
        )

        return self.__parent__._cast(_6924.HypoidGearCriticalSpeedAnalysis)

    @property
    def hypoid_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6926.HypoidGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6926,
        )

        return self.__parent__._cast(_6926.HypoidGearSetCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6928.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6928,
        )

        return self.__parent__._cast(
            _6928.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6930.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6930,
        )

        return self.__parent__._cast(
            _6930.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6931.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6931,
        )

        return self.__parent__._cast(
            _6931.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6933.KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6933,
        )

        return self.__parent__._cast(
            _6933.KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6934.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6934,
        )

        return self.__parent__._cast(
            _6934.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6936.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6936,
        )

        return self.__parent__._cast(
            _6936.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis
        )

    @property
    def mass_disc_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6937.MassDiscCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6937,
        )

        return self.__parent__._cast(_6937.MassDiscCriticalSpeedAnalysis)

    @property
    def measurement_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6938.MeasurementComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6938,
        )

        return self.__parent__._cast(_6938.MeasurementComponentCriticalSpeedAnalysis)

    @property
    def microphone_array_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6939.MicrophoneArrayCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6939,
        )

        return self.__parent__._cast(_6939.MicrophoneArrayCriticalSpeedAnalysis)

    @property
    def microphone_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6940.MicrophoneCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6940,
        )

        return self.__parent__._cast(_6940.MicrophoneCriticalSpeedAnalysis)

    @property
    def mountable_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6941.MountableComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6941,
        )

        return self.__parent__._cast(_6941.MountableComponentCriticalSpeedAnalysis)

    @property
    def oil_seal_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6942.OilSealCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6942,
        )

        return self.__parent__._cast(_6942.OilSealCriticalSpeedAnalysis)

    @property
    def part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6943.PartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6943,
        )

        return self.__parent__._cast(_6943.PartCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6945.PartToPartShearCouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6945,
        )

        return self.__parent__._cast(_6945.PartToPartShearCouplingCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6946.PartToPartShearCouplingHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6946,
        )

        return self.__parent__._cast(
            _6946.PartToPartShearCouplingHalfCriticalSpeedAnalysis
        )

    @property
    def planetary_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6948.PlanetaryGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6948,
        )

        return self.__parent__._cast(_6948.PlanetaryGearSetCriticalSpeedAnalysis)

    @property
    def planet_carrier_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6949.PlanetCarrierCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6949,
        )

        return self.__parent__._cast(_6949.PlanetCarrierCriticalSpeedAnalysis)

    @property
    def point_load_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6950.PointLoadCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6950,
        )

        return self.__parent__._cast(_6950.PointLoadCriticalSpeedAnalysis)

    @property
    def power_load_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6951.PowerLoadCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6951,
        )

        return self.__parent__._cast(_6951.PowerLoadCriticalSpeedAnalysis)

    @property
    def pulley_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6952.PulleyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6952,
        )

        return self.__parent__._cast(_6952.PulleyCriticalSpeedAnalysis)

    @property
    def ring_pins_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6953.RingPinsCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6953,
        )

        return self.__parent__._cast(_6953.RingPinsCriticalSpeedAnalysis)

    @property
    def rolling_ring_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6955.RollingRingAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6955,
        )

        return self.__parent__._cast(_6955.RollingRingAssemblyCriticalSpeedAnalysis)

    @property
    def rolling_ring_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6957.RollingRingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6957,
        )

        return self.__parent__._cast(_6957.RollingRingCriticalSpeedAnalysis)

    @property
    def root_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6958.RootAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6958,
        )

        return self.__parent__._cast(_6958.RootAssemblyCriticalSpeedAnalysis)

    @property
    def shaft_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6959.ShaftCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6959,
        )

        return self.__parent__._cast(_6959.ShaftCriticalSpeedAnalysis)

    @property
    def shaft_hub_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6960.ShaftHubConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6960,
        )

        return self.__parent__._cast(_6960.ShaftHubConnectionCriticalSpeedAnalysis)

    @property
    def specialised_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6962.SpecialisedAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6962,
        )

        return self.__parent__._cast(_6962.SpecialisedAssemblyCriticalSpeedAnalysis)

    @property
    def spiral_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6963.SpiralBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6963,
        )

        return self.__parent__._cast(_6963.SpiralBevelGearCriticalSpeedAnalysis)

    @property
    def spiral_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6965.SpiralBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6965,
        )

        return self.__parent__._cast(_6965.SpiralBevelGearSetCriticalSpeedAnalysis)

    @property
    def spring_damper_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6967.SpringDamperCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6967,
        )

        return self.__parent__._cast(_6967.SpringDamperCriticalSpeedAnalysis)

    @property
    def spring_damper_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6968.SpringDamperHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6968,
        )

        return self.__parent__._cast(_6968.SpringDamperHalfCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6969.StraightBevelDiffGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6969,
        )

        return self.__parent__._cast(_6969.StraightBevelDiffGearCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6971.StraightBevelDiffGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6971,
        )

        return self.__parent__._cast(
            _6971.StraightBevelDiffGearSetCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6972.StraightBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6972,
        )

        return self.__parent__._cast(_6972.StraightBevelGearCriticalSpeedAnalysis)

    @property
    def straight_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6974.StraightBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6974,
        )

        return self.__parent__._cast(_6974.StraightBevelGearSetCriticalSpeedAnalysis)

    @property
    def straight_bevel_planet_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6975.StraightBevelPlanetGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6975,
        )

        return self.__parent__._cast(_6975.StraightBevelPlanetGearCriticalSpeedAnalysis)

    @property
    def straight_bevel_sun_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6976.StraightBevelSunGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6976,
        )

        return self.__parent__._cast(_6976.StraightBevelSunGearCriticalSpeedAnalysis)

    @property
    def synchroniser_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6977.SynchroniserCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6977,
        )

        return self.__parent__._cast(_6977.SynchroniserCriticalSpeedAnalysis)

    @property
    def synchroniser_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6978.SynchroniserHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6978,
        )

        return self.__parent__._cast(_6978.SynchroniserHalfCriticalSpeedAnalysis)

    @property
    def synchroniser_part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6979.SynchroniserPartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6979,
        )

        return self.__parent__._cast(_6979.SynchroniserPartCriticalSpeedAnalysis)

    @property
    def synchroniser_sleeve_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6980.SynchroniserSleeveCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6980,
        )

        return self.__parent__._cast(_6980.SynchroniserSleeveCriticalSpeedAnalysis)

    @property
    def torque_converter_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6982.TorqueConverterCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6982,
        )

        return self.__parent__._cast(_6982.TorqueConverterCriticalSpeedAnalysis)

    @property
    def torque_converter_pump_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6983.TorqueConverterPumpCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6983,
        )

        return self.__parent__._cast(_6983.TorqueConverterPumpCriticalSpeedAnalysis)

    @property
    def torque_converter_turbine_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6984.TorqueConverterTurbineCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6984,
        )

        return self.__parent__._cast(_6984.TorqueConverterTurbineCriticalSpeedAnalysis)

    @property
    def unbalanced_mass_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6985.UnbalancedMassCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6985,
        )

        return self.__parent__._cast(_6985.UnbalancedMassCriticalSpeedAnalysis)

    @property
    def virtual_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6986.VirtualComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6986,
        )

        return self.__parent__._cast(_6986.VirtualComponentCriticalSpeedAnalysis)

    @property
    def worm_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6987.WormGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6987,
        )

        return self.__parent__._cast(_6987.WormGearCriticalSpeedAnalysis)

    @property
    def worm_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6989.WormGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6989,
        )

        return self.__parent__._cast(_6989.WormGearSetCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6990.ZerolBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6990,
        )

        return self.__parent__._cast(_6990.ZerolBevelGearCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6992.ZerolBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6992,
        )

        return self.__parent__._cast(_6992.ZerolBevelGearSetCriticalSpeedAnalysis)

    @property
    def abstract_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7124.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7124,
        )

        return self.__parent__._cast(
            _7124.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7125.AbstractShaftAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7125,
        )

        return self.__parent__._cast(
            _7125.AbstractShaftAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_or_housing_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7126.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7126,
        )

        return self.__parent__._cast(
            _7126.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7132.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7132,
        )

        return self.__parent__._cast(
            _7132.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7134.AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7134,
        )

        return self.__parent__._cast(
            _7134.AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7135.AssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7135,
        )

        return self.__parent__._cast(
            _7135.AssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bearing_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7137.BearingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7137,
        )

        return self.__parent__._cast(
            _7137.BearingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def belt_drive_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7139.BeltDriveAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7139,
        )

        return self.__parent__._cast(
            _7139.BeltDriveAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7140.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7140,
        )

        return self.__parent__._cast(
            _7140.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7142.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7142,
        )

        return self.__parent__._cast(
            _7142.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7143.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7143,
        )

        return self.__parent__._cast(
            _7143.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_sun_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7144.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7144,
        )

        return self.__parent__._cast(
            _7144.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7145.BevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7145,
        )

        return self.__parent__._cast(
            _7145.BevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7147.BevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7147,
        )

        return self.__parent__._cast(
            _7147.BevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bolt_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7148.BoltAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7148,
        )

        return self.__parent__._cast(
            _7148.BoltAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bolted_joint_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7149.BoltedJointAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7149,
        )

        return self.__parent__._cast(
            _7149.BoltedJointAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7150.ClutchAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7150,
        )

        return self.__parent__._cast(
            _7150.ClutchAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7152.ClutchHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7152,
        )

        return self.__parent__._cast(
            _7152.ClutchHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7154.ComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7154,
        )

        return self.__parent__._cast(
            _7154.ComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7155.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7155,
        )

        return self.__parent__._cast(
            _7155.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7157.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7157,
        )

        return self.__parent__._cast(
            _7157.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7158.ConceptGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7158,
        )

        return self.__parent__._cast(
            _7158.ConceptGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7160.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7160,
        )

        return self.__parent__._cast(
            _7160.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7161.ConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7161,
        )

        return self.__parent__._cast(
            _7161.ConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7163.ConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7163,
        )

        return self.__parent__._cast(
            _7163.ConicalGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connector_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7165.ConnectorAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7165,
        )

        return self.__parent__._cast(
            _7165.ConnectorAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7166.CouplingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7166,
        )

        return self.__parent__._cast(
            _7166.CouplingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7168.CouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7168,
        )

        return self.__parent__._cast(
            _7168.CouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7169.CVTAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7169,
        )

        return self.__parent__._cast(_7169.CVTAdvancedTimeSteppingAnalysisForModulation)

    @property
    def cvt_pulley_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7171.CVTPulleyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7171,
        )

        return self.__parent__._cast(
            _7171.CVTPulleyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7172.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7172,
        )

        return self.__parent__._cast(
            _7172.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7173.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7173,
        )

        return self.__parent__._cast(
            _7173.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7176.CylindricalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7176,
        )

        return self.__parent__._cast(
            _7176.CylindricalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7178.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7178,
        )

        return self.__parent__._cast(
            _7178.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7179.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7179,
        )

        return self.__parent__._cast(
            _7179.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def datum_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7180.DatumAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7180,
        )

        return self.__parent__._cast(
            _7180.DatumAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def external_cad_model_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7181.ExternalCADModelAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7181,
        )

        return self.__parent__._cast(
            _7181.ExternalCADModelAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7182.FaceGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7182,
        )

        return self.__parent__._cast(
            _7182.FaceGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7184.FaceGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7184,
        )

        return self.__parent__._cast(
            _7184.FaceGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def fe_part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7185.FEPartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7185,
        )

        return self.__parent__._cast(
            _7185.FEPartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def flexible_pin_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7186.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7186,
        )

        return self.__parent__._cast(
            _7186.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7187.GearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7187,
        )

        return self.__parent__._cast(
            _7187.GearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7189.GearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7189,
        )

        return self.__parent__._cast(
            _7189.GearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def guide_dxf_model_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7190.GuideDxfModelAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7190,
        )

        return self.__parent__._cast(
            _7190.GuideDxfModelAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7192.HypoidGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7192,
        )

        return self.__parent__._cast(
            _7192.HypoidGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7194.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7194,
        )

        return self.__parent__._cast(
            _7194.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7196.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7196,
        )

        return self.__parent__._cast(
            _7196.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7198.KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7198,
        )

        return self.__parent__._cast(
            _7198.KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7199.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7199,
        )

        return self.__parent__._cast(
            _7199.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7201.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7201,
        )

        return self.__parent__._cast(
            _7201.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7202.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7202,
        )

        return self.__parent__._cast(
            _7202.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7204.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7204,
        )

        return self.__parent__._cast(
            _7204.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mass_disc_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7205.MassDiscAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7205,
        )

        return self.__parent__._cast(
            _7205.MassDiscAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def measurement_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7206.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7206,
        )

        return self.__parent__._cast(
            _7206.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def microphone_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7207.MicrophoneAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7207,
        )

        return self.__parent__._cast(
            _7207.MicrophoneAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def microphone_array_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7208.MicrophoneArrayAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7208,
        )

        return self.__parent__._cast(
            _7208.MicrophoneArrayAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mountable_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7209.MountableComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7209,
        )

        return self.__parent__._cast(
            _7209.MountableComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def oil_seal_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7210.OilSealAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7210,
        )

        return self.__parent__._cast(
            _7210.OilSealAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7211.PartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7211,
        )

        return self.__parent__._cast(
            _7211.PartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7212.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7212,
        )

        return self.__parent__._cast(
            _7212.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7214.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7214,
        )

        return self.__parent__._cast(
            _7214.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planetary_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7216.PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7216,
        )

        return self.__parent__._cast(
            _7216.PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planet_carrier_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7217.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7217,
        )

        return self.__parent__._cast(
            _7217.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def point_load_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7218.PointLoadAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7218,
        )

        return self.__parent__._cast(
            _7218.PointLoadAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def power_load_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7219.PowerLoadAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7219,
        )

        return self.__parent__._cast(
            _7219.PowerLoadAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def pulley_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7220.PulleyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7220,
        )

        return self.__parent__._cast(
            _7220.PulleyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def ring_pins_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7221.RingPinsAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7221,
        )

        return self.__parent__._cast(
            _7221.RingPinsAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7223.RollingRingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7223,
        )

        return self.__parent__._cast(
            _7223.RollingRingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7224.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7224,
        )

        return self.__parent__._cast(
            _7224.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def root_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7226.RootAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7226,
        )

        return self.__parent__._cast(
            _7226.RootAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7227.ShaftAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7227,
        )

        return self.__parent__._cast(
            _7227.ShaftAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_hub_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7228.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7228,
        )

        return self.__parent__._cast(
            _7228.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def specialised_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7230.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7230,
        )

        return self.__parent__._cast(
            _7230.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7231.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7231,
        )

        return self.__parent__._cast(
            _7231.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7233.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7233,
        )

        return self.__parent__._cast(
            _7233.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7234.SpringDamperAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7234,
        )

        return self.__parent__._cast(
            _7234.SpringDamperAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7236.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7236,
        )

        return self.__parent__._cast(
            _7236.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7237.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7237,
        )

        return self.__parent__._cast(
            _7237.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7239.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7239,
        )

        return self.__parent__._cast(
            _7239.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7240.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7240,
        )

        return self.__parent__._cast(
            _7240.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7242.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7242,
        )

        return self.__parent__._cast(
            _7242.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7243.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7243,
        )

        return self.__parent__._cast(
            _7243.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_sun_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7244.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7244,
        )

        return self.__parent__._cast(
            _7244.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7245.SynchroniserAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7245,
        )

        return self.__parent__._cast(
            _7245.SynchroniserAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7246.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7246,
        )

        return self.__parent__._cast(
            _7246.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7247.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7247,
        )

        return self.__parent__._cast(
            _7247.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_sleeve_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7248.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7248,
        )

        return self.__parent__._cast(
            _7248.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7249.TorqueConverterAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7249,
        )

        return self.__parent__._cast(
            _7249.TorqueConverterAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_pump_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7251.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7251,
        )

        return self.__parent__._cast(
            _7251.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_turbine_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7252.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7252,
        )

        return self.__parent__._cast(
            _7252.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def unbalanced_mass_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7253.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7253,
        )

        return self.__parent__._cast(
            _7253.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def virtual_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7254.VirtualComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7254,
        )

        return self.__parent__._cast(
            _7254.VirtualComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7255.WormGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7255,
        )

        return self.__parent__._cast(
            _7255.WormGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7257.WormGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7257,
        )

        return self.__parent__._cast(
            _7257.WormGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7258.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7258,
        )

        return self.__parent__._cast(
            _7258.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7260.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7260,
        )

        return self.__parent__._cast(
            _7260.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7392.AbstractAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7392,
        )

        return self.__parent__._cast(_7392.AbstractAssemblyAdvancedSystemDeflection)

    @property
    def abstract_shaft_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7393.AbstractShaftAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7393,
        )

        return self.__parent__._cast(_7393.AbstractShaftAdvancedSystemDeflection)

    @property
    def abstract_shaft_or_housing_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7394.AbstractShaftOrHousingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7394,
        )

        return self.__parent__._cast(
            _7394.AbstractShaftOrHousingAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7399.AGMAGleasonConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7399,
        )

        return self.__parent__._cast(
            _7399.AGMAGleasonConicalGearAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7401.AGMAGleasonConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7401,
        )

        return self.__parent__._cast(
            _7401.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        )

    @property
    def assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7402.AssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7402,
        )

        return self.__parent__._cast(_7402.AssemblyAdvancedSystemDeflection)

    @property
    def bearing_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7403.BearingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7403,
        )

        return self.__parent__._cast(_7403.BearingAdvancedSystemDeflection)

    @property
    def belt_drive_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7405.BeltDriveAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7405,
        )

        return self.__parent__._cast(_7405.BeltDriveAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7406.BevelDifferentialGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7406,
        )

        return self.__parent__._cast(
            _7406.BevelDifferentialGearAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7408.BevelDifferentialGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7408,
        )

        return self.__parent__._cast(
            _7408.BevelDifferentialGearSetAdvancedSystemDeflection
        )

    @property
    def bevel_differential_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7409.BevelDifferentialPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7409,
        )

        return self.__parent__._cast(
            _7409.BevelDifferentialPlanetGearAdvancedSystemDeflection
        )

    @property
    def bevel_differential_sun_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7410.BevelDifferentialSunGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7410,
        )

        return self.__parent__._cast(
            _7410.BevelDifferentialSunGearAdvancedSystemDeflection
        )

    @property
    def bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7411.BevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7411,
        )

        return self.__parent__._cast(_7411.BevelGearAdvancedSystemDeflection)

    @property
    def bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7413.BevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7413,
        )

        return self.__parent__._cast(_7413.BevelGearSetAdvancedSystemDeflection)

    @property
    def bolt_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7414.BoltAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7414,
        )

        return self.__parent__._cast(_7414.BoltAdvancedSystemDeflection)

    @property
    def bolted_joint_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7415.BoltedJointAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7415,
        )

        return self.__parent__._cast(_7415.BoltedJointAdvancedSystemDeflection)

    @property
    def clutch_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7416.ClutchAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7416,
        )

        return self.__parent__._cast(_7416.ClutchAdvancedSystemDeflection)

    @property
    def clutch_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7418.ClutchHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7418,
        )

        return self.__parent__._cast(_7418.ClutchHalfAdvancedSystemDeflection)

    @property
    def component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7420.ComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7420,
        )

        return self.__parent__._cast(_7420.ComponentAdvancedSystemDeflection)

    @property
    def concept_coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7421.ConceptCouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7421,
        )

        return self.__parent__._cast(_7421.ConceptCouplingAdvancedSystemDeflection)

    @property
    def concept_coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7423.ConceptCouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7423,
        )

        return self.__parent__._cast(_7423.ConceptCouplingHalfAdvancedSystemDeflection)

    @property
    def concept_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7424.ConceptGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7424,
        )

        return self.__parent__._cast(_7424.ConceptGearAdvancedSystemDeflection)

    @property
    def concept_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7426.ConceptGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7426,
        )

        return self.__parent__._cast(_7426.ConceptGearSetAdvancedSystemDeflection)

    @property
    def conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7427.ConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7427,
        )

        return self.__parent__._cast(_7427.ConicalGearAdvancedSystemDeflection)

    @property
    def conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7429.ConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7429,
        )

        return self.__parent__._cast(_7429.ConicalGearSetAdvancedSystemDeflection)

    @property
    def connector_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7431.ConnectorAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7431,
        )

        return self.__parent__._cast(_7431.ConnectorAdvancedSystemDeflection)

    @property
    def coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7433.CouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7433,
        )

        return self.__parent__._cast(_7433.CouplingAdvancedSystemDeflection)

    @property
    def coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7435.CouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7435,
        )

        return self.__parent__._cast(_7435.CouplingHalfAdvancedSystemDeflection)

    @property
    def cvt_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7436.CVTAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7436,
        )

        return self.__parent__._cast(_7436.CVTAdvancedSystemDeflection)

    @property
    def cvt_pulley_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7438.CVTPulleyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7438,
        )

        return self.__parent__._cast(_7438.CVTPulleyAdvancedSystemDeflection)

    @property
    def cycloidal_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7439.CycloidalAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7439,
        )

        return self.__parent__._cast(_7439.CycloidalAssemblyAdvancedSystemDeflection)

    @property
    def cycloidal_disc_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7440.CycloidalDiscAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7440,
        )

        return self.__parent__._cast(_7440.CycloidalDiscAdvancedSystemDeflection)

    @property
    def cylindrical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7443.CylindricalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7443,
        )

        return self.__parent__._cast(_7443.CylindricalGearAdvancedSystemDeflection)

    @property
    def cylindrical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7445.CylindricalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7445,
        )

        return self.__parent__._cast(_7445.CylindricalGearSetAdvancedSystemDeflection)

    @property
    def cylindrical_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7447.CylindricalPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7447,
        )

        return self.__parent__._cast(
            _7447.CylindricalPlanetGearAdvancedSystemDeflection
        )

    @property
    def datum_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7448.DatumAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7448,
        )

        return self.__parent__._cast(_7448.DatumAdvancedSystemDeflection)

    @property
    def external_cad_model_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7449.ExternalCADModelAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7449,
        )

        return self.__parent__._cast(_7449.ExternalCADModelAdvancedSystemDeflection)

    @property
    def face_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7450.FaceGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7450,
        )

        return self.__parent__._cast(_7450.FaceGearAdvancedSystemDeflection)

    @property
    def face_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7452.FaceGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7452,
        )

        return self.__parent__._cast(_7452.FaceGearSetAdvancedSystemDeflection)

    @property
    def fe_part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7453.FEPartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7453,
        )

        return self.__parent__._cast(_7453.FEPartAdvancedSystemDeflection)

    @property
    def flexible_pin_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7454.FlexiblePinAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7454,
        )

        return self.__parent__._cast(_7454.FlexiblePinAssemblyAdvancedSystemDeflection)

    @property
    def gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7455.GearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7455,
        )

        return self.__parent__._cast(_7455.GearAdvancedSystemDeflection)

    @property
    def gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7457.GearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7457,
        )

        return self.__parent__._cast(_7457.GearSetAdvancedSystemDeflection)

    @property
    def guide_dxf_model_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7458.GuideDxfModelAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7458,
        )

        return self.__parent__._cast(_7458.GuideDxfModelAdvancedSystemDeflection)

    @property
    def hypoid_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7459.HypoidGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7459,
        )

        return self.__parent__._cast(_7459.HypoidGearAdvancedSystemDeflection)

    @property
    def hypoid_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7461.HypoidGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7461,
        )

        return self.__parent__._cast(_7461.HypoidGearSetAdvancedSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7463.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7463,
        )

        return self.__parent__._cast(
            _7463.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7465.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7465,
        )

        return self.__parent__._cast(
            _7465.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7466.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7466,
        )

        return self.__parent__._cast(
            _7466.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7468.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7468,
        )

        return self.__parent__._cast(
            _7468.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7469.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7469,
        )

        return self.__parent__._cast(
            _7469.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7471.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7471,
        )

        return self.__parent__._cast(
            _7471.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        )

    @property
    def mass_disc_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7473.MassDiscAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7473,
        )

        return self.__parent__._cast(_7473.MassDiscAdvancedSystemDeflection)

    @property
    def measurement_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7474.MeasurementComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7474,
        )

        return self.__parent__._cast(_7474.MeasurementComponentAdvancedSystemDeflection)

    @property
    def microphone_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7475.MicrophoneAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7475,
        )

        return self.__parent__._cast(_7475.MicrophoneAdvancedSystemDeflection)

    @property
    def microphone_array_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7476.MicrophoneArrayAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7476,
        )

        return self.__parent__._cast(_7476.MicrophoneArrayAdvancedSystemDeflection)

    @property
    def mountable_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7477.MountableComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7477,
        )

        return self.__parent__._cast(_7477.MountableComponentAdvancedSystemDeflection)

    @property
    def oil_seal_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7478.OilSealAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7478,
        )

        return self.__parent__._cast(_7478.OilSealAdvancedSystemDeflection)

    @property
    def part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7479.PartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7479,
        )

        return self.__parent__._cast(_7479.PartAdvancedSystemDeflection)

    @property
    def part_to_part_shear_coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7480.PartToPartShearCouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7480,
        )

        return self.__parent__._cast(
            _7480.PartToPartShearCouplingAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7482.PartToPartShearCouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7482,
        )

        return self.__parent__._cast(
            _7482.PartToPartShearCouplingHalfAdvancedSystemDeflection
        )

    @property
    def planetary_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7484.PlanetaryGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7484,
        )

        return self.__parent__._cast(_7484.PlanetaryGearSetAdvancedSystemDeflection)

    @property
    def planet_carrier_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7485.PlanetCarrierAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7485,
        )

        return self.__parent__._cast(_7485.PlanetCarrierAdvancedSystemDeflection)

    @property
    def point_load_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7486.PointLoadAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7486,
        )

        return self.__parent__._cast(_7486.PointLoadAdvancedSystemDeflection)

    @property
    def power_load_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7487.PowerLoadAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7487,
        )

        return self.__parent__._cast(_7487.PowerLoadAdvancedSystemDeflection)

    @property
    def pulley_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7488.PulleyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7488,
        )

        return self.__parent__._cast(_7488.PulleyAdvancedSystemDeflection)

    @property
    def ring_pins_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7489.RingPinsAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7489,
        )

        return self.__parent__._cast(_7489.RingPinsAdvancedSystemDeflection)

    @property
    def rolling_ring_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7491.RollingRingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7491,
        )

        return self.__parent__._cast(_7491.RollingRingAdvancedSystemDeflection)

    @property
    def rolling_ring_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7492.RollingRingAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7492,
        )

        return self.__parent__._cast(_7492.RollingRingAssemblyAdvancedSystemDeflection)

    @property
    def root_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7494.RootAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7494,
        )

        return self.__parent__._cast(_7494.RootAssemblyAdvancedSystemDeflection)

    @property
    def shaft_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7495.ShaftAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7495,
        )

        return self.__parent__._cast(_7495.ShaftAdvancedSystemDeflection)

    @property
    def shaft_hub_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7496.ShaftHubConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7496,
        )

        return self.__parent__._cast(_7496.ShaftHubConnectionAdvancedSystemDeflection)

    @property
    def specialised_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7498.SpecialisedAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7498,
        )

        return self.__parent__._cast(_7498.SpecialisedAssemblyAdvancedSystemDeflection)

    @property
    def spiral_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7499.SpiralBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7499,
        )

        return self.__parent__._cast(_7499.SpiralBevelGearAdvancedSystemDeflection)

    @property
    def spiral_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7501.SpiralBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7501,
        )

        return self.__parent__._cast(_7501.SpiralBevelGearSetAdvancedSystemDeflection)

    @property
    def spring_damper_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7502.SpringDamperAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7502,
        )

        return self.__parent__._cast(_7502.SpringDamperAdvancedSystemDeflection)

    @property
    def spring_damper_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7504.SpringDamperHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7504,
        )

        return self.__parent__._cast(_7504.SpringDamperHalfAdvancedSystemDeflection)

    @property
    def straight_bevel_diff_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7505.StraightBevelDiffGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7505,
        )

        return self.__parent__._cast(
            _7505.StraightBevelDiffGearAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7507.StraightBevelDiffGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7507,
        )

        return self.__parent__._cast(
            _7507.StraightBevelDiffGearSetAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7508.StraightBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7508,
        )

        return self.__parent__._cast(_7508.StraightBevelGearAdvancedSystemDeflection)

    @property
    def straight_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7510.StraightBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7510,
        )

        return self.__parent__._cast(_7510.StraightBevelGearSetAdvancedSystemDeflection)

    @property
    def straight_bevel_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7511.StraightBevelPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7511,
        )

        return self.__parent__._cast(
            _7511.StraightBevelPlanetGearAdvancedSystemDeflection
        )

    @property
    def straight_bevel_sun_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7512.StraightBevelSunGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7512,
        )

        return self.__parent__._cast(_7512.StraightBevelSunGearAdvancedSystemDeflection)

    @property
    def synchroniser_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7513.SynchroniserAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7513,
        )

        return self.__parent__._cast(_7513.SynchroniserAdvancedSystemDeflection)

    @property
    def synchroniser_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7514.SynchroniserHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7514,
        )

        return self.__parent__._cast(_7514.SynchroniserHalfAdvancedSystemDeflection)

    @property
    def synchroniser_part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7515.SynchroniserPartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7515,
        )

        return self.__parent__._cast(_7515.SynchroniserPartAdvancedSystemDeflection)

    @property
    def synchroniser_sleeve_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7516.SynchroniserSleeveAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7516,
        )

        return self.__parent__._cast(_7516.SynchroniserSleeveAdvancedSystemDeflection)

    @property
    def torque_converter_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7517.TorqueConverterAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7517,
        )

        return self.__parent__._cast(_7517.TorqueConverterAdvancedSystemDeflection)

    @property
    def torque_converter_pump_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7519.TorqueConverterPumpAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7519,
        )

        return self.__parent__._cast(_7519.TorqueConverterPumpAdvancedSystemDeflection)

    @property
    def torque_converter_turbine_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7520.TorqueConverterTurbineAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7520,
        )

        return self.__parent__._cast(
            _7520.TorqueConverterTurbineAdvancedSystemDeflection
        )

    @property
    def unbalanced_mass_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7522.UnbalancedMassAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7522,
        )

        return self.__parent__._cast(_7522.UnbalancedMassAdvancedSystemDeflection)

    @property
    def virtual_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7523.VirtualComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7523,
        )

        return self.__parent__._cast(_7523.VirtualComponentAdvancedSystemDeflection)

    @property
    def worm_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7524.WormGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7524,
        )

        return self.__parent__._cast(_7524.WormGearAdvancedSystemDeflection)

    @property
    def worm_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7526.WormGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7526,
        )

        return self.__parent__._cast(_7526.WormGearSetAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7527.ZerolBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7527,
        )

        return self.__parent__._cast(_7527.ZerolBevelGearAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7529.ZerolBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7529,
        )

        return self.__parent__._cast(_7529.ZerolBevelGearSetAdvancedSystemDeflection)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_7675.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7675,
        )

        return self.__parent__._cast(_7675.AbstractAssemblyLoadCase)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_7676.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7676,
        )

        return self.__parent__._cast(_7676.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_7677.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7677,
        )

        return self.__parent__._cast(_7677.AbstractShaftOrHousingLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7682.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7682,
        )

        return self.__parent__._cast(_7682.AGMAGleasonConicalGearLoadCase)

    @property
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7684.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7684,
        )

        return self.__parent__._cast(_7684.AGMAGleasonConicalGearSetLoadCase)

    @property
    def assembly_load_case(self: "CastSelf") -> "_7687.AssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7687,
        )

        return self.__parent__._cast(_7687.AssemblyLoadCase)

    @property
    def bearing_load_case(self: "CastSelf") -> "_7688.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7688,
        )

        return self.__parent__._cast(_7688.BearingLoadCase)

    @property
    def belt_drive_load_case(self: "CastSelf") -> "_7690.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7690,
        )

        return self.__parent__._cast(_7690.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_7691.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7691,
        )

        return self.__parent__._cast(_7691.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7693.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7693,
        )

        return self.__parent__._cast(_7693.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7694.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7694,
        )

        return self.__parent__._cast(_7694.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7695.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7695,
        )

        return self.__parent__._cast(_7695.BevelDifferentialSunGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_7696.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7696,
        )

        return self.__parent__._cast(_7696.BevelGearLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_7698.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7698,
        )

        return self.__parent__._cast(_7698.BevelGearSetLoadCase)

    @property
    def bolted_joint_load_case(self: "CastSelf") -> "_7699.BoltedJointLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7699,
        )

        return self.__parent__._cast(_7699.BoltedJointLoadCase)

    @property
    def bolt_load_case(self: "CastSelf") -> "_7700.BoltLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7700,
        )

        return self.__parent__._cast(_7700.BoltLoadCase)

    @property
    def clutch_half_load_case(self: "CastSelf") -> "_7702.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7702,
        )

        return self.__parent__._cast(_7702.ClutchHalfLoadCase)

    @property
    def clutch_load_case(self: "CastSelf") -> "_7703.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7703,
        )

        return self.__parent__._cast(_7703.ClutchLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7706,
        )

        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7708.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7708,
        )

        return self.__parent__._cast(_7708.ConceptCouplingHalfLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_7709.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7709,
        )

        return self.__parent__._cast(_7709.ConceptCouplingLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_7710.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConceptGearLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_7712.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConceptGearSetLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_7713.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConicalGearLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_7717.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7717,
        )

        return self.__parent__._cast(_7717.ConicalGearSetLoadCase)

    @property
    def connector_load_case(self: "CastSelf") -> "_7719.ConnectorLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7719,
        )

        return self.__parent__._cast(_7719.ConnectorLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7721.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7721,
        )

        return self.__parent__._cast(_7721.CouplingHalfLoadCase)

    @property
    def coupling_load_case(self: "CastSelf") -> "_7722.CouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7722,
        )

        return self.__parent__._cast(_7722.CouplingLoadCase)

    @property
    def cvt_load_case(self: "CastSelf") -> "_7724.CVTLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7724,
        )

        return self.__parent__._cast(_7724.CVTLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7725.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7725,
        )

        return self.__parent__._cast(_7725.CVTPulleyLoadCase)

    @property
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7726.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7726,
        )

        return self.__parent__._cast(_7726.CycloidalAssemblyLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7728.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7728,
        )

        return self.__parent__._cast(_7728.CycloidalDiscLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7730.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7730,
        )

        return self.__parent__._cast(_7730.CylindricalGearLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7734.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7734,
        )

        return self.__parent__._cast(_7734.CylindricalGearSetLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7735.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7735,
        )

        return self.__parent__._cast(_7735.CylindricalPlanetGearLoadCase)

    @property
    def datum_load_case(self: "CastSelf") -> "_7738.DatumLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7738,
        )

        return self.__parent__._cast(_7738.DatumLoadCase)

    @property
    def external_cad_model_load_case(
        self: "CastSelf",
    ) -> "_7752.ExternalCADModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7752,
        )

        return self.__parent__._cast(_7752.ExternalCADModelLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7753.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7753,
        )

        return self.__parent__._cast(_7753.FaceGearLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7755.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7755,
        )

        return self.__parent__._cast(_7755.FaceGearSetLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7756.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7756,
        )

        return self.__parent__._cast(_7756.FEPartLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7757.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7757,
        )

        return self.__parent__._cast(_7757.FlexiblePinAssemblyLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7759.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7759,
        )

        return self.__parent__._cast(_7759.GearLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7764.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7764,
        )

        return self.__parent__._cast(_7764.GearSetLoadCase)

    @property
    def guide_dxf_model_load_case(self: "CastSelf") -> "_7765.GuideDxfModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7765,
        )

        return self.__parent__._cast(_7765.GuideDxfModelLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7774.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7774,
        )

        return self.__parent__._cast(_7774.HypoidGearLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7776.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7776,
        )

        return self.__parent__._cast(_7776.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7781.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7781,
        )

        return self.__parent__._cast(_7781.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7783.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7783,
        )

        return self.__parent__._cast(
            _7783.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7784.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7784,
        )

        return self.__parent__._cast(_7784.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7786,
        )

        return self.__parent__._cast(
            _7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7787.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7787,
        )

        return self.__parent__._cast(
            _7787.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7789,
        )

        return self.__parent__._cast(
            _7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def mass_disc_load_case(self: "CastSelf") -> "_7790.MassDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7790,
        )

        return self.__parent__._cast(_7790.MassDiscLoadCase)

    @property
    def measurement_component_load_case(
        self: "CastSelf",
    ) -> "_7791.MeasurementComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7791,
        )

        return self.__parent__._cast(_7791.MeasurementComponentLoadCase)

    @property
    def microphone_array_load_case(self: "CastSelf") -> "_7793.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7793,
        )

        return self.__parent__._cast(_7793.MicrophoneArrayLoadCase)

    @property
    def microphone_load_case(self: "CastSelf") -> "_7794.MicrophoneLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7794,
        )

        return self.__parent__._cast(_7794.MicrophoneLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7795.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7795,
        )

        return self.__parent__._cast(_7795.MountableComponentLoadCase)

    @property
    def oil_seal_load_case(self: "CastSelf") -> "_7797.OilSealLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7797,
        )

        return self.__parent__._cast(_7797.OilSealLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7801.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7801,
        )

        return self.__parent__._cast(_7801.PartToPartShearCouplingHalfLoadCase)

    @property
    def part_to_part_shear_coupling_load_case(
        self: "CastSelf",
    ) -> "_7802.PartToPartShearCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7802,
        )

        return self.__parent__._cast(_7802.PartToPartShearCouplingLoadCase)

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7804.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7804,
        )

        return self.__parent__._cast(_7804.PlanetaryGearSetLoadCase)

    @property
    def planet_carrier_load_case(self: "CastSelf") -> "_7806.PlanetCarrierLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7806,
        )

        return self.__parent__._cast(_7806.PlanetCarrierLoadCase)

    @property
    def point_load_load_case(self: "CastSelf") -> "_7809.PointLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7809,
        )

        return self.__parent__._cast(_7809.PointLoadLoadCase)

    @property
    def power_load_load_case(self: "CastSelf") -> "_7810.PowerLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7810,
        )

        return self.__parent__._cast(_7810.PowerLoadLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7811.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7811,
        )

        return self.__parent__._cast(_7811.PulleyLoadCase)

    @property
    def ring_pins_load_case(self: "CastSelf") -> "_7814.RingPinsLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7814,
        )

        return self.__parent__._cast(_7814.RingPinsLoadCase)

    @property
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7816.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7816,
        )

        return self.__parent__._cast(_7816.RollingRingAssemblyLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7818.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7818,
        )

        return self.__parent__._cast(_7818.RollingRingLoadCase)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "_7819.RootAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7819,
        )

        return self.__parent__._cast(_7819.RootAssemblyLoadCase)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "_7820.ShaftHubConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7820,
        )

        return self.__parent__._cast(_7820.ShaftHubConnectionLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7821.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7821,
        )

        return self.__parent__._cast(_7821.ShaftLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7823.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7823,
        )

        return self.__parent__._cast(_7823.SpecialisedAssemblyLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7824.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7824,
        )

        return self.__parent__._cast(_7824.SpiralBevelGearLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7826.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7826,
        )

        return self.__parent__._cast(_7826.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7828.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7828,
        )

        return self.__parent__._cast(_7828.SpringDamperHalfLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7829.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7829,
        )

        return self.__parent__._cast(_7829.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7830.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7830,
        )

        return self.__parent__._cast(_7830.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7832.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7832,
        )

        return self.__parent__._cast(_7832.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7833.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7833,
        )

        return self.__parent__._cast(_7833.StraightBevelGearLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7835.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7835,
        )

        return self.__parent__._cast(_7835.StraightBevelGearSetLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7836.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7836,
        )

        return self.__parent__._cast(_7836.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7837.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7837,
        )

        return self.__parent__._cast(_7837.StraightBevelSunGearLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7838.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7838,
        )

        return self.__parent__._cast(_7838.SynchroniserHalfLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7839.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7839,
        )

        return self.__parent__._cast(_7839.SynchroniserLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7840.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7840,
        )

        return self.__parent__._cast(_7840.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7841.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7841,
        )

        return self.__parent__._cast(_7841.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7845.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7845,
        )

        return self.__parent__._cast(_7845.TorqueConverterLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7846.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7846,
        )

        return self.__parent__._cast(_7846.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7847.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7847,
        )

        return self.__parent__._cast(_7847.TorqueConverterTurbineLoadCase)

    @property
    def unbalanced_mass_load_case(self: "CastSelf") -> "_7852.UnbalancedMassLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7852,
        )

        return self.__parent__._cast(_7852.UnbalancedMassLoadCase)

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7853.VirtualComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7853,
        )

        return self.__parent__._cast(_7853.VirtualComponentLoadCase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_7854.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7854,
        )

        return self.__parent__._cast(_7854.WormGearLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7856.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7856,
        )

        return self.__parent__._cast(_7856.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7857.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7857,
        )

        return self.__parent__._cast(_7857.ZerolBevelGearLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7859.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7859,
        )

        return self.__parent__._cast(_7859.ZerolBevelGearSetLoadCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7889.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7889,
        )

        return self.__parent__._cast(_7889.PartFEAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7891.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7891,
        )

        return self.__parent__._cast(_7891.PartTimeSeriesLoadAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "PartAnalysis":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class PartAnalysis(_2894.DesignEntitySingleContextAnalysis):
    """PartAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def planetary_original(self: "Self") -> "PartAnalysis":
        """mastapy.system_model.analyses_and_results.PartAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetaryOriginal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartAnalysis
        """
        return _Cast_PartAnalysis(self)
