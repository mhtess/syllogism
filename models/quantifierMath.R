?factorial


trinomial <- function(i,j,k){
 return(factorial(i+j+k)/(factorial(i)*factorial(j)*factorial(k)) )
}

trinomial(1,2,1)


noUtt <- function(n, p){
  x <- p*(1-p)
  y <- (1-p)*p
  z <- (1-p)*(1-p)
  total <- 0
  for (i in 1:(n-1)){
    for (j in 1:(n-i)){
      k <- n-i-j
      prob <- trinomial(i,j,k)*(x^i)*(y^j)*(z^k)
      total <- total + prob
    }
  }
  return (total)
}

allUtt <- function(n, p){
  x <- p*p
  y <- (1-p)*p
  z <- (1-p)*(1-p)
  total <- 0
  for (i in 1:n){
    for (j in 0:(n-i)){
      k <- n-i-j
      prob <- trinomial(i,j,k)*(x^i)*(y^j)*(z^k)
      total <- total + prob
    }
  }
  return (total)
}




noUtt(5,0.5)


someA <- function(n,p){
  return (1 - ((1-p)^n))
}

noUttEI <- function(n,p){
 return (noUtt(n,p) / (someA(n,p)*someA(n,p)))
}


allUttEI <- function(n,p){
  return (allUtt(n,p) / (someA(n,p)*someA(n,p)))
}


noUttEI(3,0.5)
allUttEI(4,0.89)
