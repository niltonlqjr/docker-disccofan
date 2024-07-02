#include <FreeImage.h>
#include <argp.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>


struct Arguments{
    int *factors;
    char *filename;
    char *output_file;
    char *img_ext;
};

void upcase_string(char *str){
    int i;
    for(i=0;i<strlen(str);i++){
        str[i] = toupper(str[i]);
    }
}



void vector_from_string(char *str, char sep, int **ret, int *size){
    int i, *vec;
    char *pch;
    char delim[2]={sep, '\0'};
    *size = 1;
    for(i=0; i < strlen(str); i++){
        if(str[i] == sep){
            (*size)++;
        }
    }
    vec = (int*)calloc(*size, sizeof(int));
    *ret = vec;
    i=0;
    pch = strtok (str,delim);
    while (pch != NULL){
        vec[i++] = atoi(pch);
        pch = strtok (NULL, delim);
    }
    return;
}

/** Generic image loader
@param lpszPathName Pointer to the full file name
@param flag Optional load flag constant
@return Returns the loaded dib if successful, returns NULL otherwise
*/
FIBITMAP* GenericLoader(const char* lpszPathName, int flag,  bool convertToGreyScale) {
    FIBITMAP *tmp = NULL, *dib;
    FREE_IMAGE_FORMAT fif = FIF_UNKNOWN;
    // check the file signature and deduce its format
    // (the second argument is currently not used by FreeImage)
    fif = FreeImage_GetFileType(lpszPathName, 0);
    if(fif == FIF_UNKNOWN) {
        // no signature ?
        // try to guess the file format from the file extension
        fif = FreeImage_GetFIFFromFilename(lpszPathName);
    }
    // check that the plugin has reading capabilities ...
    if((fif != FIF_UNKNOWN) && FreeImage_FIFSupportsReading(fif)) {
        // ok, let's load the file
        tmp = FreeImage_Load(fif, lpszPathName, flag);
        // unless a bad file format, we are done !
    }
    dib=tmp;
    if(convertToGreyScale && tmp){
        dib = FreeImage_ConvertToGreyscale(tmp);
        FreeImage_Unload(tmp);
    }
    return dib;
}

bool GenericSaver(FIBITMAP* img, const char *path, int flag){
    FREE_IMAGE_FORMAT fif = FIF_UNKNOWN;
    // check the file signature and deduce its format
    // (the second argument is currently not used by FreeImage)
    fif = FreeImage_GetFileType(path, 0);
    if(fif == FIF_UNKNOWN) {
        // no signature ?
        // try to guess the file format from the file extension
        fif = FreeImage_GetFIFFromFilename(path);
    }
    // check that the plugin has reading capabilities ...
    if((fif != FIF_UNKNOWN) && FreeImage_FIFSupportsWriting(fif)) {
        // ok, let's load the file
        return FreeImage_Save(fif, img, path, flag);
        // unless a bad file format, we are done !
    }
    return false;
}


static int parse_args(int key, char *arg, struct argp_state *state){

    struct Arguments *program_args = state->input;
    int *dims, dims_size, len;

    if(key == 'f'){
        vector_from_string(arg, ',', &dims, &dims_size);
        if(dims_size != 2){
            printf("The number of dimensions of downscale factor must be 2");
            exit(0);
        }
        program_args->factors = dims;
    }else if(key == 'o'){
        len = strlen(arg);
        program_args->output_file = (char*) malloc(len * sizeof(char));
        strncpy(program_args->output_file, arg, len);
    }else if(key == ARGP_KEY_ARG){
        len = strlen(arg);
        program_args->filename = (char*) malloc(len * sizeof(char));
        strncpy(program_args->filename, arg, len);
    }else if(key == ARGP_KEY_NO_ARGS){
        argp_usage(state);
    }
    return 0;
}


int main(int argc, char **argv){
    struct argp_option args_opts[] = {
        {0,'f',"DIMS",0,"Downscale factor comma separated"},
        {0,'o',"FILENAME",0,"Output file name"},
        {0}
    };
    int default_dim[] = {2,2};

    struct Arguments program_args;

    program_args.factors = default_dim;
    program_args.output_file = "saida.png";

    struct argp args = {args_opts, parse_args, 0, 0};
    
    argp_parse(&args, argc, argv, 0, 0, &program_args);
    
    char *filename = program_args.filename;
    char *output = program_args.output_file;
    char *img_ext = program_args.img_ext;
    int *factors = program_args.factors;
    
    FIBITMAP *img, *rescale;

    printf("Input:%s \nOutput:%s\n",filename,output);
    printf("Reduction factor: (%d,%d)\n", factors[0], factors[1]);

    img = GenericLoader(filename,0,true);

    if(img == NULL){
        printf("Error loading the image %s\n",filename);
        exit(0);
    }

    unsigned int img_w = FreeImage_GetWidth(img);
    unsigned int img_h = FreeImage_GetHeight(img);

    printf("Rescaling from (%d, %d) to (%d, %d)\n",img_w,img_h,
                        img_w/factors[0], img_h/factors[1]);

    rescale = FreeImage_Rescale(img, img_w/factors[0], img_h/factors[1],FILTER_BOX);
    FreeImage_Unload(img);

    if(!GenericSaver(rescale, output, 0)){
        printf("Error saving image %s\n",output);
        exit(0);
    }else{
        printf("Image %s saved successfully\n",output);
    }
    FreeImage_Unload(rescale);
    return 0;
}