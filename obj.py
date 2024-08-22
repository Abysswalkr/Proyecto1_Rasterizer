class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in lines:
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue

            try:
                prefix, value = line.split(" ", 1)
            except ValueError:
                continue

            if prefix == "v":  # Vertices
                vert = list(map(float, value.split()))
                self.vertices.append(vert)

            elif prefix == "vt":  # Texture coordinates
                vts = list(map(float, value.split()))
                self.texcoords.append([vts[0], vts[1]])

            elif prefix == "vn":  # Normals
                norm = list(map(float, value.split()))
                self.normals.append(norm)

            elif prefix == "f":  # Faces
                face = []
                verts = value.split()
                for vert in verts:
                    vert = [int(v) if v else None for v in vert.split("/")]
                    face.append(vert)
                self.faces.append(face)
