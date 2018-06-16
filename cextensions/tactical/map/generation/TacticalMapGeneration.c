#include <Python.h>


int generate(int height, int width, int maxheight, int mountains, int hills, int forests, int rivers, int towns, int roads) {
	int h, i, j, k, g; //iteration indices
	int x, y;
	float temp, tempa, tempb, tempc, tempd, tempe, tempf, tempy, tempx;
	
	float **map = malloc(sizeof(*float) * 4); //array of each map type: height, forest, river, town
	float *heightmap = malloc(sizeof(float) * height * width);
	float *forestmap = malloc(sizeof(float) * height * width);
	float *rivermap = malloc(sizeof(float) * height * width);
	float *townmap = malloc(sizeof(float) * height * width);
	
	map[0] = heightmap;
	map[1] = forestmap;
	map[2] = rivermap;
	map[3] = townmap;


	//Height map
	if (1) {
		//set zero
		for (i = 0; i < width; i++) {
			for (j = 0; j < height; j++) {
				heightmap[i*height + j] = 0;
			}
		}

		//gradual slope
		for (h = 0; h < 3; h++) {
			temp = rand() % 11 - 5.1;
			tempa = rand() % 11 - 5.1;

			for (i = 0; i < width; i++) {
				for (j = 0; j < height; j++) {
					heightmap[i*height + j] += abs(float((temp * i + tempa * j))) / (abs(temp*width) + abs(tempa*height)) * 2;
				}
			}
		}

		//generate mountians
		if (mountains > 0) {
			for (h = 0; h < max((int)(mountains / 6.0), 1)) {
				temp = rand() % 2;
				tempa = rand() % 2;

				tempb = rand() % (width*0.45) + width * 0.3;
				tempc = rand() % (height*0.45) + height * 0.3;

				tempd = rand() % (width*0.45) + width * 0.3;
				tempe = rand() % (height*0.45) + height * 0.3;

				i = 0;
				while (i < = mountains) {
					i++;

					//first
					if (1) {
						tempy = rand() % (int)(height*0.9 - tempc) + tempc;

						if (temp == 1) {
							tempx = rand() % max((int)(tempb - (height - tempy)*(tempb / (height - tempc))), (int)(width*0.3));
						}
						else {
							tempf = min((int)(tempb + (height - 1 - tempy)*((width-1-tempb)/(height-1-tempc))), (int)(width*0.75));
							tempx = rand() % (width - tempf) + tempf;
						}
						heightmap[tempx*height + tempy] = maxheight;
					}
					
					//second
					if (i > 2) {
						temp_y = rand() % (int)(tempe - height * 0.2) + (int)(height * 0.2);

						if (tempa == 1) {
							tempx = rand() % max((int)(tempd - tempy * (tempd / tempe)), (int)(height * 0.3));
						}
						else {
							tempf = min((int)(tempd + tempy * ((width - 1 - tempd) / tempe)), (int)(height * 0.75));
							tempx = rand() % (width - tempf) + tempf;
						}
						heightmap[tempx*height + tempy] = maxheight;
					}
				}
			}
		}

		//generate hills
		for (i = 0; i < hills; i++) {
			heightmap[(rand() % (int)(width*0.7) + (int)(width*0.15)) * height + (rand() % (int)(height*0.7) + (int)(height*0.15))] = maxheight * 0.8;
		}

		//rough terrain
		for (h = 0; h < 20; h++) {
			if (rand() % 2 == 0) {
				temp = 1;
			}
			else {
				temp = 0;
			}

			for (i = 0; i < width - 1; i++) {
				for (j = 0; j < height - 1; j++) {

					if (temp == 1) {
						x = width - 1 - i;
						y = height - 1 - j;
					}
					else {
						x = i;
						y = j;
					}
					tempa = 0;
					tempb = 0;

					for (g = -1; g < 2; g++) {
						for (k = -1; k < 2; k++) {

							if (k != 0 || g != 0) {
								if (x + g >= 0 && x + g < width && y + k >= 0 && y + k < height) {
									tempb++;
									tempa = max(tempa, heightmap[(x + g)*height + y + k]);
								}
							}
							if (tempa > heightmap[x*height + y]) {
								heightmap[x*height + y] = self.tempa * (rand() % 10 + 5) / (tempb + 1);
							}

						}
					}
				}
			}
		}

		//smoothing 1
		for (h = 0; h < 10; h++) {
			if (rand() % 2 == 0) {
				temp = 1;
			}
			else {
				temp = 0;
			}
			for (i = 0; i < width - 1; i++) {
				for (j = 0; j < height - 1; j++) {
					if (temp == 1) {
						x = width - 1 - i;
						y = height - 1 - j;
					}
					else {
						x = i;
						y = j;
					}

					tempa = 0;
					tempb = max_height;

					if (heightmap[x*height + y] != maxheight || rand() % 4 == 3) {
						for (g = -1; g < 2; g++) {
							for (k = -1; k < 2; k++) {

								if (k != 0 || g != 0) {
									if (x + g >= 0 && x + g < width && y + k >= 0 && y + k < height) {
										tempa = max(tempa, heightmap[(x + g)*height + (y + k)]);
										tempb = min(tempb, heightmap[(x + g)*height + y + k]);
									}
								}

								if (rand() % 20 > 0) {
									heightmap[x*height + y] = (heightmap[x*height + y] * 3 + tempa + tempb) / 5;
								}
								else {
									heightmap[x*height + y] = tempa;
								}
							}
						}
					}
				}
			}
		}

		//smoothing 2
		for (h = 0; h < 4; h++) {
			if (rand() % 2 == 0) {
				temp = 1;
			}
			else {
				temp = 0;
			}
			for (i = 0; i < width - 1; i++) {
				for (j = 0; j < height - 1; j++) {
					if (temp == 1) {
						x = width - 1 - i;
						y = height - 1 - j;
					}
					else {
						x = i;
						y = j;
					}
					tempa = 0;
					tempb = 0;

					for (g = -1; g < 2; g++) {
						for (k = -1; k < 2; k++) {

							if (k != 0 || g != 0) {
								if (x + g >= 0 && x + g < width && y + k >= 0 && y + k < height) {
									tempa += heightmap[(x + g)*height + y + k];
									tempb++;
								}
							}
						}
					}
					heightmap[x*height + y] = (heightmap[x*height + y] * 4 + tempa / tempb) / 5;
				}
			}
		}

		//edge smoothing
		for (h = 1; h < 2; h++) {
			for (i = 0; i < width - 1; i++) {
				for (j = 0; j < height; j++) {
					if (i != 0) {
						heightmap[i*height + j] = (heightmap[(i - h)*height + j] + heightmap[i*height + j]) / 2;
					}
					else {
						heightmap[i*height + j] = (heightmap[(i + h)*height + j] + heightmap[i*height + j]) / 2;
					}
				}
			}

			for (i = 0; i < width; i++) {
				for (j = 0; j < height-1; j++) {
					if (j != 0) {
						heightmap[i*height + j] = (heightmap[(i)*height + j - h] + heightmap[i*height + j]) / 2;
					}
					else {
						heightmap[i*height + j] = (heightmap[(i)*height + j + h] + heightmap[i*height + j]) / 2;
					}
				}
			}
		}
	}
}

static PyObject * TacticalMapGeneration_generate(PyObject *self, PyObject *args){
	int height, width,result;

	if(!PyArg_ParseTuple(args,"ii", &height, &width)){
		return NULL;
	}
	result = generate(height, width);

	return PyLong_FromLong(result);
}

static PyMethodDef TacticalMapGenerationMethods[] = {

	{"solid", TacticalMapGeneration_generate, METH_VARARGS,"Execute a shell command"},
	{NULL,NULL,0,NULL}

};

static struct PyModuleDef TacticalMapGenerationmodule = {
	PyModuleDef_HEAD_INIT,
	"TacticalMapGeneration",
	NULL,
	-1,

	TacticalMapGenerationMethods
};

PyMODINIT_FUNC PyInit_TacticalMapGeneration(void){
	return PyModule_Create(&TacticalMapGenerationmodule);
}

int main(int argc, char *argv[])
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("TacticalMapGeneration", PyInit_TacticalMapGeneration);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyImport_ImportModule("TacticalMapGeneration");

    PyMem_RawFree(program);
    return 0;
}