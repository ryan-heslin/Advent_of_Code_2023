setClass("Rational", 
         slots = c(numerators = "array", 
         denominators = "array", dim = "integer"), 
         #prototype = list(numerators  = 0L, 
         #denominators = 1L,  dim = 1L)
)
setValidity("Rational", function(object){
    num_length <- if(is.matrix(object@numerators)) dim(object@numerators) else length(object@numerators)
    denom_length <- if(is.matrix(object@denominators)) dim(object@denominators) else length(object@denominators)
    if(identical(num_length, 0L) || identical(denom_length, 0L)){ 
        "Numerator and denominator must have length at least 1"
} else if(!identical(num_length, denom_length) && !(identical(num_length, 1L) || identical(denom_length, 1L) )){
        "Numerators and denominators must have the same length"
    
    }else if(any(object@denominators == 0)){ 
        "Denominators cannot contain 0"
    } else{
        TRUE
    }
})

Rational <- function(numerators, denominators){ 
num_length <- if(is.matrix(numerators)) dim(numerators) else length(numerators)
denom_length <- if(is.matrix(denominators)) dim(denominators) else length(denominators)

    # Recycle unit numerator or denominator
    if(identical(num_length, 1L) && !identical(num_length , denom_length)){ 
        numerators <- array(numerators, dim = denom_length)
    }else if (identical(denom_length, 1L) && !identical(denom_length , num_length)){ 
        denominators <- array(denominators, dim = num_length)
    }
    names(numerators) <- NULL
    names(denominators) <- NULL
    dims <- if(is.matrix(denominators)) dim(denominators) else length(denominators)
    new("Rational", numerators = numerators, denominators = denominators, dim = dims)  |> 
        simplify()
}

 #setGeneric("dim", function(x) standardGeneric("dim"))
setGeneric("numerators", function(x) standardGeneric("numerators"))
setGeneric("denominators", function(x) standardGeneric("denominators"))
setGeneric("numerators<-", function(x, ...) standardGeneric("numerators<-"), signature = "x")
setGeneric("denominators<-", function(x, ...) standardGeneric("denominators<-"), signature = "x")
setGeneric("simplify", function(x) standardGeneric("simplify"))

setMethod("numerators", "Rational", function(x) x@numerators)
setMethod("numerators<-", "Rational", function(x, value) Rational(x@numerators, value))
setMethod("denominators", "Rational", function(x) x@denominators)
setMethod("denominators<-", "Rational", function(x, value) Rational(x@numerators, value))
setMethod("dim", "Rational", function(x) x@dim  )
setMethod("simplify", "Rational", function(x){ 
    gcds <- mapply(numerators(x), denominators(x), FUN = gcd)
    dim(gcds) <- x@dim
    x@numerators <- x@numerators %/% gcds
    x@denominators <- x@denominators %/% gcds
    validObject(x)
    x
})


 setMethod("show", "Rational", function(object){ 
    dims <- dim(object)
    left <- as.character(object@numerators)
    right <- as.character(object@denominators)
    combined <- matrix(paste0(left, "/", right), nrow = dims[[1]])
    print(combined)
    invisible()
})

gcd <- function(a, b){
    while (b != 0){
        t  <- b
        b <- a %% b
        a <- t
    }
    a
}

simplify_matrix <- function(A){
    divisors <- matrix(vapply(A, \(x) gcd(Re(x), Im(x)), FUN.VALUE = numeric(1)), nrow = nrow(A))
    A * (1 / matrix(divisors, nrow = nrow(A)))
}

frac_divide <- function(num, denom){
    complex(real = Re(num) * Im(denom), imaginary = Im(num) * Re(denom))
}

frac_multiply <- function(x, y){ 
    complex(real = Re(x) * Re(y), imaginary = Im(x) * Im(y))
}

frac_subtract <- function(x, y){ 
    complex(real = (Re(x) * Im(y)) - ((Im(x) * Re(y))), imaginary = Im(x) * Im(y))
}
frac_add <- function(x, y){ 
complex(real = (Re(x) * Im(y)) + ((Im(x) * Re(y))), imaginary = Im(x) * Im(y))
}

rref <- function(A){
    pivot <- 1
    n <- dim(A)[[1]]
    m <- dim(A)[[2]]
    numerators <- A 
    # Real is numerator, imag is denominator
    result <- A + 1i
    denoms <- matrix(1, nrow = n, ncol = m)

    # TODO reorder by leading ones
    for(pivot in seq(1, n)){ 
        # Scale to 1
        result[pivot, pivot:m] <- frac_divide(result[pivot, pivot:m], result[pivot, pivot])
        # Subtract from lower row
        current <- result[pivot, seq(pivot, m)]
        # Clear leading values below
        if (pivot < n){
        for (below in seq(pivot + 1, n)){ 
            factor <- result[below, pivot]
            result[below, seq(pivot, m)]  <-
                frac_subtract(result[below, seq(pivot, m)], frac_multiply(factor, current))

    }
        }
}
result
}

back_solve <- function(A){
    n <- nrow(A)
    m <- ncol(A)
    col <- m -1

    solution <- rep(0+1i, n)
    for (row in rev(seq_len(n))){ 
       rhs  <-  A[row ,m] 
       if (col != m- 1){ 
           rhs <-  frac_subtract(rhs, Reduce(x = frac_multiply(A[row, (col + 1):(m-1)], solution[(row +1) :n]), f=  frac_add))
       }
       solution[[row]] <- frac_divide(rhs, A[row, col])
       col <- col - 1
    }
    solution
}

my_solve <- function(A){ 
    result <- back_solve(rref(A))
    Re(result) / Im(result)
}

test <- function(A, b){
    stopifnot(all.equal(my_solve(cbind(A, b)), solve(A, b)))
}

for (i in seq(0, 100)){ 
    A <- matrix(sample(seq(0, 100000), replace = FALSE, size = 12), nrow = 3)
    test(A[,-4], A[,4])
}




find_intersection <- function(pair, low, high) {
    A_pos <- pair[[1]][[1]][-3]
    A_vel <- pair[[1]][[2]][-3]
    B_pos <- pair[[2]][[1]][-3]
    B_vel <- pair[[2]][[2]][-3]
    left <- -A_vel
    b <- A_pos - B_pos
    A <- cbind(left, B_vel)

    # Beta in OLS
    solution <- tryCatch(solve(A, b), error = function(e) {
    })
    if (is.null(solution) || (solution[[1]] < 0) || (solution[[2]] < 0)) {
        return()
    }
    intersection <- A_pos + A_vel * solution[[1]]

    if (all((intersection >= low) & (intersection <= high))) {
        intersection
    } else {
        return()
    }
}

to_int <- function(string) {
    strsplit(string, ",\\s?") |>
        unlist() |>
        as.numeric()
}

parse <- function(line) {
    parts <- strsplit(line, "\\s@\\s") |>
        unlist() |>
        lapply(to_int)
}

# Y DX - X DY = x dy - y dx + Y dx + y DX - x DY - X dy
# (dy'-dy) X + (dx-dx') Y + (y-y') DX + (x'-x) DY = x' dy' - y' dx' - x dy + y dx
# See https://www.reddit.com/r/adventofcode/comments/18q40he/2023_day_24_part_2_a_straightforward_nonsolver/
make_row <- function(pair, first, second) {
    c1 <- pair[[1]][[1]][[first]]
    d1 <- pair[[1]][[2]][[first]]
    c1_prime <- pair[[2]][[1]][[first]]
    d1_prime <- pair[[2]][[2]][[first]]

    c2 <- pair[[1]][[1]][[second]]
    d2 <- pair[[1]][[2]][[second]]
    c2_prime <- pair[[2]][[1]][[second]]
    d2_prime <- pair[[2]][[2]][[second]]

    rhs <- (c1_prime * d2_prime) - (c2_prime * d1_prime) - (c1 * d2) + (c2 * d1)
    c(d2_prime - d2, d1 - d1_prime, c2 - c2_prime, c1_prime - c1, rhs)
}

find_coord <- function(pairs, first, second) {
    equations <- c()
    # Try until we find a coordinate pair where equation can be solved
    for (pair in pairs) {
        row <- make_row(pair, first, second)
        new <- rbind(equations, row)
        if (qr(new)[["rank"]] == nrow(new)) {
            equations <- new
        }
        if (length(equations) && nrow(equations) == 4) break
    }
    # Solve for X, Y, ignore velocities
    result <- solve(equations[, -5], equations[, 5])
    reduced <- simplify_matrix(rref(equations))
    # My complex number hack for rational numbers
    solution <- back_solve(reduced)
    Re(solution[1:2]) / Im(solution[1:2])
    # print(result)
    # result[1:2]
}

solve_part2 <- function(pairs) {
    start <- find_coord(pairs, 1, 2)
    second <- find_coord(rev(pairs), 1, 3)
    c(start[1:2], second[[2]])
}

raw_input <- readLines("inputs/day24.txt")
parsed <- lapply(raw_input, parse)
lower <- 200000000000000
upper <- 400000000000000
pairs <- combn(parsed, m = 2, FUN = c, simplify = FALSE)
part1 <- lapply(pairs, find_intersection, low = lower, high = upper) |>
    vapply(Negate(is.null), FUN.VALUE = logical(1)) |>
    sum()
print(part1)

part2 <- solve_part2(pairs)
cat(as.character(sum(part2)), "\n")
