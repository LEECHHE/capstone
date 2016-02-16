# Capstone
##TO-DO List
1. Bayesian Network 공부
2. K2 Algorithm - Bayesian Network Learning을 위한 알고리즘
3. 간단한 Sample Network 만들기
	- Sample Network(Asia network 등)으로 얻은 데이터로 Network를 다시 만드는 것까지
- Additional : K2를 제외한 다른 BN Learning 알고리즘 찾아보기
	- BNC Algorithm : Hill Climbing과 비슷한 방법
		- conditional log likelihood의 class를 primary objective function으로 활용
		- 빈 네트워크에서 각 단계마다 arc를 추가하고 삭제하거나 방향을 반대로 바꾼다.

##Reference
- Bayes Server[[링크](http://www.bayesserver.com/BayesianNetworks.aspx)]
	- 들어가서 [Live web example](http://www.bayesserver.com/Live.aspx) 클릭하면 Sample Network도 있음.
- K2 in Parallel[[Link](https://cs205k2project.wordpress.com/the-k2-algorithm/)]
	- github : https://github.com/Schec/K2-in-Parallel
	- 여기서 [K2_serial.py](https://github.com/Schec/K2-in-Parallel/blob/master/k2_serial.py) 사용

##진행 상황
- Iris dataset : python k2_serial.py -D ../dataset/iris/Iris.csv -u 4
	- 약 2분 가까이 걸리며, P_old, P_new 값이 음수인 이유는 이 코드에선 소수를 로그로 변환하여 계산.