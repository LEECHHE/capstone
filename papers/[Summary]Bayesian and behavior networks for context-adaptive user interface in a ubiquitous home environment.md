#Bayesian and behavior networks for context-adaptive user interface in a ubiquitous home environment

##Introduction
- context-adaptive UI
- Ubiquitous home 환경에서 location과 device 정보를 이용 
	- Bayesian Network를 통해 주어진 환경에서 devices의 필요성 예측
	- behavior network를 통해 현재 환경에서 해당 device의 필요한 기능 선택

## Related Works
###Bayesian Networks for context-awareness
#### 용어 정의
	Context : Entity의 상황을 charactterize할 수 있는 정보
	Entity : User와 Application 사이의 Interaction과 관련 있는 사람, 장소, object 등

- 복잡한 domain에서 불확실성을 handling하는데 사용. 특히 context-awareness.
- 변수에 해당하는 노드와 arc(연결된 노드 사이의 확률적 연관성)으로 DAG로 구성.
- network를 train할 데이터가 없어도 domain knowledge를 기반으로 modeling 될 수 있음.

###Behavior Networks
- Node는 5개의 요소로 구성
	- Precondition : active되어야 하는 module을 순서대로 true로 set
	- Add list : 모듈이 active 되었을 때 true가 되었을 때 condition들의 list.
	- Delete List : module이 active되었을 때 false로 setting.
	- Activation Level
	- Executable code : 모든 precondition이 true가 되었을 때 실행됨.

## Context-adaptive UI for a ubiquitous home environment
### Modeling a ubiquitous home environment
- E={Location_List,Device_List,Sensor_List}
- Location_List={Location1,Location2,...,LocationN}
- Device_List={Device1,Device2,...,DeviceN}
- Sensor_List={Sensor1,Sensor2,...,SensorN}
- Location={Location_Name,Location_ID,Neighbors}
- Device={Device_Name,Device_ID,Location_ID,Function_List}
- Function_List={Function1,Function2,...,FunctionN}
- Function={Function_Name,Function_ID,Function_Type, Function_Value, Add_List, Delete_List}
- Sensor={Sensor_Name,Sensor_ID,Sensor_Type,Sensor_Value}

### Predicting the neccessary devices using a Bayesian Network
- 주어진 context에서 필요한 device를 추론하는데 network 사용.
- 일반적으로, 데이터로 bayesian network를 training하는 건 2단계로 구성
	1. structure를 train
	- 주어진 데이터와 잘 맞는 network structure를 찾는 것으로 해결.
	- 잘 맞는 건 여러 score metrics를 사용하는데, 이 metrics와 잘 맞는지는 Greedy로 확인
	- **이 Greedy 알고리즘 중 하나가 K2 알고리즘**

	2. parameter set을 train

### Selecting necessary functions using a behavior network
이 뒤로 무슨 말인지 모르겠다...
