#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>

#define MANAGER 0
#define TAG_ASK_FOR_NUMBER 1
#define TAG_SEND_NUMBER 2
#define TAG_SEND_ANSWER 3

MPI_Datatype MPI_answer,MPI_task;

typedef struct task{
    long long int num;
    int valid;
}task;

typedef struct answer{
    long long int num;
    int primo;
}answer;
int primo(long long int n){
    long long int i;
    for(i=2;i<n;i++){
        if(n%i == 0){
            return 0;
        }
    }
    return 1;
}
void worker(int id){
    answer a;
    task t;
    MPI_Status st;
    while(1){
        MPI_Send(&a,1,MPI_answer,MANAGER,TAG_ASK_FOR_NUMBER,
                 MPI_COMM_WORLD);
        MPI_Recv(&t,1,MPI_task,MANAGER,TAG_SEND_NUMBER,
                 MPI_COMM_WORLD,&st);
        if(!t.valid){
            break;
        }
        a.num = t.num;
        a.primo = primo(a.num);
        MPI_Send(&a,1,MPI_answer,MANAGER,TAG_SEND_ANSWER,
        MPI_COMM_WORLD);
    }
}
void manager(long long int *vet, int size_vet,int num_workers){
    int s,done,tag,i,sender, *finished;
    finished = (int*)calloc(num_workers,sizeof(int));
    answer ans;
    task t;
    MPI_Status st;
    done = 0;
    i=0;
    for(s=0;s<num_workers;s++){
        finished[s]=0;
    }
    while(done < size_vet){
        MPI_Recv(&ans,1,MPI_answer,MPI_ANY_SOURCE,MPI_ANY_TAG,
                 MPI_COMM_WORLD,&st);
        sender=st.MPI_SOURCE;
        tag=st.MPI_TAG;
        if(tag == TAG_ASK_FOR_NUMBER){
            if(i<size_vet){
                t.num = vet[i];
                t.valid = 1;
                MPI_Send(&t,1,MPI_task,sender,TAG_SEND_NUMBER,
                         MPI_COMM_WORLD);
                i++;
                
            }else{
                t.valid=0;
                finished[sender]=1;
                MPI_Send(&t,1,MPI_task,sender,TAG_SEND_NUMBER,
                         MPI_COMM_WORLD);
            }
        }else if(tag == TAG_SEND_ANSWER){/
            done++;
            if(ans.primo){
                printf("%lld is a prime number (answer given by process :%d)\n",ans.num,sender);
            }
        } 
    }
    finished[0]=1;
    int num_finished = 0;
    for(s=0;s<num_workers;s++)
        num_finished+=finished[s];
    while(num_finished < num_workers){
        MPI_Recv(&ans,1,MPI_answer,MPI_ANY_SOURCE,MPI_ANY_TAG,
                 MPI_COMM_WORLD,&st);
        t.valid=0;
        sender=st.MPI_SOURCE;
        MPI_Send(&t,1,MPI_task,sender,TAG_SEND_NUMBER,
                 MPI_COMM_WORLD);
        num_finished++;
    }
    printf("end of manager process!\n");  
}
int main(int argc, char *argv[]){
    MPI_Init(&argc, &argv);
    long long int *v;
    int tot_num,i,size, id;
    tot_num=atoi(argv[1]);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&id);
    int lengths[2] = {1,1};
    MPI_Datatype types[2]={MPI_LONG_LONG_INT,MPI_INT};
    MPI_Aint desloc_ans[2], desloc_task[2];
    desloc_ans[0]=offsetof(answer,num);
    desloc_ans[1]=offsetof(answer,primo);
    MPI_Type_create_struct(2,lengths,desloc_ans,types,&MPI_answer);
    MPI_Type_commit(&MPI_answer);
    desloc_task[0]=offsetof(task,num);
    desloc_task[1]=offsetof(task,valid);
    MPI_Type_create_struct(2,lengths,desloc_task,types,&MPI_task);
    MPI_Type_commit(&MPI_task);
    if(id==MANAGER){
        srand(time(NULL));
        printf("numeros:%d\n",tot_num);
        v=(long long int*)malloc(tot_num*sizeof(long long int));
        for(i=0;i<tot_num;i++)
            v[i]=rand()%10000000+10000000;
        manager(v,tot_num,size);
    }else
        worker(id);
    MPI_Type_free(&MPI_answer);  
    MPI_Type_free(&MPI_task); 
    MPI_Finalize();
}


        
