*   A generative network model of neurodevelopmental diversity in structural brain organization

    

# Data source

The test data were download from [OSF | A generative network model of neurodevelopmental diversity in structural brain organization](https://osf.io/h9px4/?view_only=984260dcff444b59819961ece9c724ec)



# Generative model

the original generative model can be found in 

*   http://www.pnas.org/cgi/doi/10.1073/pnas.1111738109
*   https://linkinghub.elsevier.com/retrieve/pii/S1053811915008563

It's a simple two-variable generative model.



# About `bct` package in python

Frequently, an error occurred when I use `generative_model()` function, so I modify the source code and check the result. The test environment is:

*   python 3.8.12
*   numpy 1.20.3
*   scipy 1.6.2

Generally, there are two problem:

*   the input __seed network__ `A `  would be modified by `*_gen()` function after running, so I add `A = A.copy()` at the beginning for every `*_gen()` function

*   index error

    ```
    # example in "euclidean_gen"
    
    for i in range(mseed, m):
    	C = np.append(0, np.cumsum(P[u, v]))
    	#r = np.sum(rng.random_sample()*C[-1] >= C)
    	r = np.sum(rng.random_sample()*C[-1] >= C) - 1 # modified by duzc
    	b[i] = r
    	P = Fd
    	#P[u[b[:i]], v[b[:i]]] = P[v[b[:i]], u[b[:i]]] = 0
    	P[u[b[:i+1]], v[b[:i+1]]] = P[v[b[:i+1]], u[b[:i+1]]] = 0 # modified by duzc
    
    	A[u[r], v[r]] = A[v[r], u[r]] = 1
    ```

It seems fine after fix. The test code is `test_bct_duzc.py` 

he modified package were renamed as `bct_duzc`

