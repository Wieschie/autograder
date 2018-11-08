#include <iostream>
#include <vector>

using namespace std;

int main(int argc, char *argv[]){
	int n_vec = 10;
	if (argc > 1)
		n_vec = stoi(argv[1]);
	vector<vector<double>> v(n_vec);
	for (int i = 0; i < n_vec; i++){
		v[i].reserve(1024);
		cout << "Allocating v[" << i << "]." << endl;
	}	

}


