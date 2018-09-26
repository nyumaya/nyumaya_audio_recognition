#include <ctime>
#include <iostream>
#include <cstdlib>  

#include "nyumaya_lib.h"


int main (int argc, char *argv[])
{

	AudioRecognition *ar = new AudioRecognition(argv[1]);
	//ar->ProfileRun();

	clock_t begin = clock();

	for (int i = 0 ; i < 100 ; i++){
		// Run inference
		int16_t data_test[3200];
		for(int i = 0; i < 3200; ++i)
		{
			data_test[i] = (std::rand() - 16384)/1000.0 ;
		}
		ar->RunDetection(data_test,3200);
		std::cout << "OK: " << i << std::endl;
	}


	clock_t end = clock();
	double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << "Time taken: " << elapsed_secs << std::endl;
	

	return 0;
}
