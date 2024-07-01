#include <FreeImage.h>
#include <argp.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int *vector_from_string(char *str, char sep){
    int *ret, i, num_dim=1;
    for(i=0; i< strlen(str); i++){
        if(str[i] == sep){
            num_dim++;
        }
    }
    ret = (int*)malloc(num_dim * sizeof(int));
    return ret;
}

static int parse_args(int key, char *arg, struct argp_state *state){
    switch(key){
        case 'f': 
    }
    return 0;
}


int main(int argc, char **argv){
    struct argp_option args_opts[] = {
        {0,'f',"DIMS",0,"Dimensions comma separated"},
        {0}
    };
    struct argp args = {args_opts, parse_args, 0, 0};
    return argp_parse(&args, argc, argv, 0, 0, 0);
}
