import torch


def sqnorm(a):
    return torch.sum(a**2)


def edge_squared_circumradius(edge):
    return sqnorm(edge[0] - edge[1]) / 4


def triangle_squared_circumradius_2d(triangle):
    a = triangle[0] - triangle[1]
    b = triangle[1] - triangle[2]
    c = triangle[2] - triangle[0]
    cross = a[0] * b[1] - b[0] * a[1]
    return sqnorm(a) * sqnorm(b) * sqnorm(c) / (4 * cross**2)


def triangle_squared_circumradius_3d(triangle):
    a = triangle[0] - triangle[1]
    b = triangle[1] - triangle[2]
    c = triangle[2] - triangle[0]
    cross = torch.linalg.cross(a, b)
    return sqnorm(a) * sqnorm(b) * sqnorm(c) / (4 * sqnorm(cross))


def tetrahedron_squared_circumradius_3d(tetrahedron):
    D = torch.vstack(
        [
            torch.sum(tetrahedron**2, 1),
            tetrahedron.transpose(0, 1),
            torch.ones(4, dtype=float),
        ]
    )
    a = torch.det(D[[1, 2, 3, 4]])
    c = torch.det(D[[0, 1, 2, 3]])
    Dx = torch.det(D[[0, 2, 3, 4]])
    Dy = -torch.det(D[[0, 1, 3, 4]])
    Dz = torch.det(D[[0, 1, 2, 4]])
    return (Dx**2 + Dy**2 + Dz**2 - 4 * a * c) / (4 * (a**2))
