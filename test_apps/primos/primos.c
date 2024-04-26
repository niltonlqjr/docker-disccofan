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
                 MPI_COMM_WORLD);//solicita tarefa ao gerente
        MPI_Recv(&t,1,MPI_task,MANAGER,TAG_SEND_NUMBER,
                 MPI_COMM_WORLD,&st);//recebe tarefa do gerente
        if(!t.valid){
            break;
        }
        a.num = t.num;
        a.primo = primo(a.num);
        MPI_Send(&a,1,MPI_answer,MANAGER,TAG_SEND_ANSWER,
        MPI_COMM_WORLD);//envia resposta ao gerente
    }//final do laço
}
void manager(long long int *vet, int size_vet,int num_workers){
    int s,done,tag,i,sender, *finished;
    finished = (int*)calloc(num_workers,sizeof(int));
    answer ans;
    task t;
    MPI_Status st;
    done = 0;//nenhuma tarefa feita
    i=0;//nenhuma tarefa enviada
    for(s=0;s<num_workers;s++){
        finished[s]=0;
    }//nenhum trabalhador terminou sua execução;
    while(done < size_vet){
        MPI_Recv(&ans,1,MPI_answer,MPI_ANY_SOURCE,MPI_ANY_TAG,
                 MPI_COMM_WORLD,&st);//recebe mensagem do trabalhador
        sender=st.MPI_SOURCE;//avalia qual trabalhador enviou
        tag=st.MPI_TAG;//avalia a tag enviada
        if(tag == TAG_ASK_FOR_NUMBER){//se a tag for uma solicitação 
            if(i<size_vet){//verifica se ja enviou todos números
            //caso não tenha enviado
                t.num = vet[i];
                t.valid = 1;
                MPI_Send(&t,1,MPI_task,sender,TAG_SEND_NUMBER,
                         MPI_COMM_WORLD);//envia o número atual
                i++;
                
            }else{// caso ja tenha enviado todos numeros
                t.valid=0;//seta sinal de bolsa vazia
                finished[sender]=1;
                MPI_Send(&t,1,MPI_task,sender,TAG_SEND_NUMBER,
                         MPI_COMM_WORLD);//envia sinal de bolsa vazia;
            }
        }else if(tag == TAG_SEND_ANSWER){//caso seja um envio de resposta
            done++;//incrementa a quantidade de tarefas terminadas
                    //mostra resultado
            if(ans.primo){
                printf("%lld e primo segundo processo:%d\n",ans.num,sender);
            }
        } //fim  if then else para verificar tag
    }//fim while
    finished[0]=1;//marca processo gerente como terminado (saiu do laço)
    int num_finished = 0;
    for(s=0;s<num_workers;s++)// conta quantidade de processos que terminaram
        num_finished+=finished[s];
    while(num_finished < num_workers){
        MPI_Recv(&ans,1,MPI_answer,MPI_ANY_SOURCE,MPI_ANY_TAG,
                 MPI_COMM_WORLD,&st);//aguarda processos que nao 
                                    //terminaram solicitarem nova tarefa
        t.valid=0;//seta sinal de bolsa vazia
        sender=st.MPI_SOURCE;
        MPI_Send(&t,1,MPI_task,sender,TAG_SEND_NUMBER,
                 MPI_COMM_WORLD);//envia sinal de bolsa vazia 
        num_finished++;
    }
    printf("fim do manager!\n");  
}// fim do gerente
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


        
