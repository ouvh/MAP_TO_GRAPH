import math
import numpy
import random,time


def get_sphere_vertex(center:tuple,radius:float,layer_precision:float,curve_precision:float) -> list[tuple]:

    limit_error = 0
    start = center[2] - radius + limit_error
    end = center[2] + radius - limit_error
    layer = [ [ (center[0] + (math.sqrt(radius**2 - (start + i*((end-start)/layer_precision) - center[2])**2)) * math.cos(j*((2*math.pi)/curve_precision) + ( i*((math.pi)/curve_precision) )),center[1] + (math.sqrt(radius**2 - (start + i*((end-start)/layer_precision) - center[2])**2)) * math.sin(j*((2*math.pi)/curve_precision) + ( i*((math.pi)/curve_precision) )),start + i*((end-start)/layer_precision) ) for j in range(curve_precision)] for i in range(layer_precision + 1)]
    triangles = []

    for i in range(layer_precision):
        for j in range(curve_precision):
            triangles.append((layer[i][j],layer[i+1][j],layer[i][(j+1)%curve_precision]))
        
        for j in range(curve_precision):
            triangles.append((layer[i+1][j],layer[i][j],layer[i+1][(j+1)%curve_precision])[::-1])
       
    vertex = sum(triangles,start=tuple())

    
    normals = [(1,1,1) for _ in range(len(vertex))]

    vertex = numpy.array(vertex, dtype='f4')
    normals = numpy.array(normals, dtype='f4')
    vertex_data = numpy.hstack([normals, vertex])
    return vertex_data




def get_icosahedron(s,center,):
    rotation_vector = (0,0,1)
    angle = 2*(math.pi/5)
    temp_angle = math.pi/5
    inside_length = s / (2 * math.sin(math.pi/5))
    h = (s**2 - inside_length**2)**0.5

    top_center = (center[0],center[1],center[2] + 2*h)
    top_middle_center = (center[0],center[1],center[2] + h)
    bottom_center = (center[0],center[1],center[2] - 2*h)
    bottom_middle_center = (center[0],center[1],center[2] - h)
    

    rotation_matrice = [
        [rotation_vector[0]**2 + (1 - rotation_vector[0]**2) * math.cos(angle), rotation_vector[0]*rotation_vector[1]*(1 - math.cos(angle)) - rotation_vector[2]*math.sin(angle), rotation_vector[0]*rotation_vector[2]*(1 - math.cos(angle)) + rotation_vector[1]*math.sin(angle)],
        [rotation_vector[0]*rotation_vector[1]*(1 - math.cos(angle)) + rotation_vector[2]*math.sin(angle), rotation_vector[1]**2 + (1 - rotation_vector[1]**2) * math.cos(angle), rotation_vector[1]*rotation_vector[2]*(1 - math.cos(angle)) - rotation_vector[0]*math.sin(angle)],
        [rotation_vector[0]*rotation_vector[2]*(1 - math.cos(angle)) - rotation_vector[1]*math.sin(angle), rotation_vector[1]*rotation_vector[2]*(1 - math.cos(angle)) + rotation_vector[0]*math.sin(angle), rotation_vector[2]**2 + (1 - rotation_vector[2]**2) * math.cos(angle)]
    ]
    temp = [
        [rotation_vector[0]**2 + (1 - rotation_vector[0]**2) * math.cos(temp_angle), rotation_vector[0]*rotation_vector[1]*(1 - math.cos(temp_angle)) - rotation_vector[2]*math.sin(temp_angle), rotation_vector[0]*rotation_vector[2]*(1 - math.cos(temp_angle)) + rotation_vector[1]*math.sin(temp_angle)],
        [rotation_vector[0]*rotation_vector[1]*(1 - math.cos(temp_angle)) + rotation_vector[2]*math.sin(temp_angle), rotation_vector[1]**2 + (1 - rotation_vector[1]**2) * math.cos(temp_angle), rotation_vector[1]*rotation_vector[2]*(1 - math.cos(temp_angle)) - rotation_vector[0]*math.sin(temp_angle)],
        [rotation_vector[0]*rotation_vector[2]*(1 - math.cos(temp_angle)) - rotation_vector[1]*math.sin(temp_angle), rotation_vector[1]*rotation_vector[2]*(1 - math.cos(temp_angle)) + rotation_vector[0]*math.sin(temp_angle), rotation_vector[2]**2 + (1 - rotation_vector[2]**2) * math.cos(temp_angle)]
    ]



    top_points = []

    rotating_vector = (inside_length,0,0)
    for i in range(5):
        top_points.append(somme_de_vecteur(top_middle_center,rotating_vector))
        rotating_vector = produit_matrice(rotation_matrice,rotating_vector)
    

    bottom_points = []
    rotating_vector = produit_matrice(temp,(inside_length,0,0))
    for i in range(5):
        bottom_points.append(somme_de_vecteur(bottom_middle_center,rotating_vector))
        rotating_vector = produit_matrice(rotation_matrice,rotating_vector)

    triangles = [(top_points[0],top_points[1],top_center),(top_points[1],top_points[2],top_center),(top_points[2],top_points[3],top_center),(top_points[3],top_points[4],top_center),(top_points[4],top_points[0],top_center),
                 (bottom_points[0],bottom_center,bottom_points[1]),(bottom_points[1],bottom_center,bottom_points[2]),(bottom_points[2],bottom_center,bottom_points[3]),(bottom_points[3],bottom_center,bottom_points[4]),(bottom_points[4],bottom_center,bottom_points[0]),
                 (bottom_points[4],top_points[0],bottom_points[0]),(bottom_points[0],top_points[1],bottom_points[1]),(bottom_points[1],top_points[2],bottom_points[2]),(bottom_points[2],top_points[3],bottom_points[3]),(bottom_points[3],top_points[4],bottom_points[4]),
                 (top_points[0],bottom_points[0],top_points[1]),(top_points[1],bottom_points[1],top_points[2]),(top_points[2],bottom_points[2],top_points[3]),(top_points[3],bottom_points[3],top_points[4]),(top_points[4],bottom_points[4],top_points[0])]

    vertex = sum(triangles,start=tuple())
    #normals = [(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)) for _ in range(len(vertex))]
    normals = sum([(calculate_normal(i),)*3 for i in triangles],start=tuple())

    vertex = numpy.array(vertex, dtype='f4')
    normals = numpy.array(normals, dtype='f4')
    vertex_data = numpy.hstack([normals, vertex])
    
    return vertex_data







def get_tunnel(center1:tuple,center2:tuple,thickness:float) -> list[tuple]:
    angle = (2*math.pi)/3
    normal = (center2[0] - center1[0],center2[1] - center1[1],center2[2] - center1[2])
    e = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    normal_1 = (normal[0]/e,normal[1]/e,normal[2]/e)

    d = -(normal[0]*center1[0] + normal[1]*center1[1] + normal[2]*center1[2])




    if normal[2] == 0:
        if normal[1] == 0:
            vecteur_directeur = (-d/normal[0],1,1)
            if vecteur_directeur == center1:
                vecteur_directeur = (-d/normal[0],1,2)

        else:
            vecteur_directeur = (1,-(d+normal[0])/normal[1],0)

            if vecteur_directeur == center1:
                vecteur_directeur = (2,-(d+2*normal[0])/normal[1],0)
    else:
        vecteur_directeur = (1,1,((-normal[0] - normal[1] - d)/normal[2]))

        if vecteur_directeur == center1:
            vecteur_directeur = (1,2,((-normal[0] - 2*normal[1] - d)/normal[2]))















    vecteur_directeur = (vecteur_directeur[0] - center1[0],vecteur_directeur[1] - center1[1],vecteur_directeur[2] - center1[2])

    norme = math.sqrt(vecteur_directeur[0]**2 + vecteur_directeur[1]**2 + vecteur_directeur[2]**2)
    vecteur_directeur = ((vecteur_directeur[0]/norme)*thickness,(vecteur_directeur[1]/norme)*thickness,(vecteur_directeur[2]/norme)*thickness)

    matrice = [
        [normal_1[0]**2 + (1 - normal_1[0]**2) * math.cos(angle), normal_1[0]*normal_1[1]*(1 - math.cos(angle)) - normal_1[2]*math.sin(angle), normal_1[0]*normal_1[2]*(1 - math.cos(angle)) + normal_1[1]*math.sin(angle)],
        [normal_1[0]*normal_1[1]*(1 - math.cos(angle)) + normal_1[2]*math.sin(angle), normal_1[1]**2 + (1 - normal_1[1]**2) * math.cos(angle), normal_1[1]*normal_1[2]*(1 - math.cos(angle)) - normal_1[0]*math.sin(angle)],
        [normal_1[0]*normal_1[2]*(1 - math.cos(angle)) - normal_1[1]*math.sin(angle), normal_1[1]*normal_1[2]*(1 - math.cos(angle)) + normal_1[0]*math.sin(angle), normal_1[2]**2 + (1 - normal_1[2]**2) * math.cos(angle)]
    ]

    vector1 = vecteur_directeur
    vector2 = produit_matrice(matrice,vector1)
    vector3 = produit_matrice(matrice,vector2)

    point_1 = somme_de_vecteur(center1, vector1)
    dual_point_1 = somme_de_vecteur(center2, vector1)

    point_2 = somme_de_vecteur(center1, vector2)
    dual_point_2 = somme_de_vecteur(center2, vector2)

    point_3 = somme_de_vecteur(center1, vector3)
    dual_point_3 = somme_de_vecteur(center2, vector3)


    triangles = [(point_2,dual_point_1,point_1),(point_2,dual_point_2,dual_point_1),(point_3,dual_point_1,dual_point_3),(point_1,dual_point_1,point_3),(point_2,dual_point_3,point_3),(point_2,dual_point_2,dual_point_3)]

    vertex = sum(triangles,start=tuple())
    normals = [(1,1,1) for _ in range(len(vertex))]

    vertex = numpy.array(vertex, dtype='f4')
    normals = numpy.array(normals, dtype='f4')
    vertex_data = numpy.hstack([normals, vertex])

    return vertex_data


def produit_matrice(matrice,vect):
    return (matrice[0][0]*vect[0] + matrice[0][1]*vect[1] + matrice[0][2]*vect[2],matrice[1][0]*vect[0] + matrice[1][1]*vect[1] + matrice[1][2]*vect[2],matrice[2][0]*vect[0] + matrice[2][1]*vect[1] + matrice[2][2]*vect[2])


def somme_de_vecteur(ver1,ver2):
    return (ver1[0] + ver2[0],ver1[1] + ver2[1],ver1[2] + ver2[2])

def calculate_normal(points):
    vector = [(points[1][0] - points[0][0],points[1][1] - points[0][1],points[1][2] - points[0][2]),(points[2][0] - points[0][0],points[2][1] - points[0][1],points[2][2] - points[0][2])]
    vectori = (vector[0][1]*vector[1][2] - vector[1][1]*vector[0][2],  - vector[0][0]*vector[1][2]  + vector[1][0]*vector[0][2],vector[0][0]*vector[1][1] - vector[1][0]*vector[0][1])
    norme = (vectori[0]**2 + vectori[1]**2)**0.5
    return (vectori[0]/norme,vectori[1]/norme,vectori[2]/norme)

def blender_test():
    

    file1 = "C:\\Users\\Oussama Laaroussi\\Desktop\\blender_module\\vertices.txt"
    file2 = "C:\\Users\\Oussama Laaroussi\\Desktop\\blender_module\\faces.txt"



    def get_list(txtname):
        listname = []
        with open(txtname) as f:
            for line in f:
                line = line.rstrip(",\r\n") . replace("(","").replace(")","").replace(" ","")
                row  = list(line.split(","))
                listname. append (row)
        listname = [[float(j) for j in i] for i in listname]
        return listname


    points = get_list(file1)
    print(points)
    triangles = list(map(lambda x:(points[int(x[0])],points[int(x[1])],points[int(x[2])]),get_list(file2)))

    vertex = sum(triangles,start=tuple())
    normals = [(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)) for _ in range(len(vertex))]

    vertex = numpy.array(vertex, dtype='f4')
    normals = numpy.array(normals, dtype='f4')
    vertex_data = numpy.hstack([normals, vertex])
    
    return vertex_data

    







