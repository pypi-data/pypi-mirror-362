import os

import pytest

from homcloud.view_vectorized_PD import main, argument_parser


@pytest.mark.integration
def test_main(datadir, picture_dir):
    vect_path = os.path.join(datadir, "vect.txt")
    info_path = os.path.join(datadir, "histoinfo.json")
    pict_path = str(picture_dir.joinpath("view_vectorized_PD_0.png"))
    main(argument_parser().parse_args(["-o", pict_path, vect_path, info_path]))
