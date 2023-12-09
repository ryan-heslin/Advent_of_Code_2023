impute <- function(sequence) {
    modulus <- 1
    part1 <- sequence[[length(sequence)]]
    part2 <- sequence[[1]]

    while (any(sequence)) {
        # To avoid numeric(0)
        sequence <- diff(sequence)
        part1 <- part1 + sequence[[length(sequence)]]
        part2 <- part2 + (sequence[[1]] * (1 - (2 * modulus)))
        modulus <- (modulus + 1) %% 2
    }
    c(part1, part2)
}

raw <- read.table("inputs/day9.txt", sep = " ") |>
    as.matrix() |>
    unname() |>
    asplit(MARGIN = 1)

result <- vapply(raw, impute, FUN.VALUE = array(NA_real_, dim = 2)) |>
    rowSums()
print(result[[1]])
print(result[[2]])
