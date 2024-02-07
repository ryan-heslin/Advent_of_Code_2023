distance <- function(pair, empty_rows, empty_cols, iterations = 1) {
    pair <- rbind(pair[[1]], pair[[2]])
    xes <- sort(pair[, 2])
    ys <- sort(pair[, 1])
    sum(abs(pair[1, ] - pair[2, ])) +
        (iterations * (sum(empty_cols > xes[[1]] & empty_cols < xes[[2]]) +
            sum(empty_rows > ys[[1]] & empty_rows < ys[[2]])))
}

solve <- function(grid, iterations = 1) {
    pairs <- which(grid, arr.ind = TRUE)
    rows <- which(rowSums(grid) == 0)
    cols <- which(colSums(grid) == 0)
    asplit(pairs, MARGIN = 1) |>
        combn(m = 2, FUN = \(x) distance(x, rows, cols,
            iterations = iterations
        )) |>
        sum()
}

raw <- readLines("inputs/day11.txt") |>
    strsplit(split = "") |>
    do.call(what = rbind)
raw <- raw == "#"
part1 <- solve(raw)
print(part1)

iterations <- 1000000
part2 <- solve(raw, iterations - 1)
print(part2)
