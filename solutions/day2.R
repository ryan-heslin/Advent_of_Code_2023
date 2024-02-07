colors <- c("red" = 0, "green" = 0, "blue" = 0)

parse_pairs <- function(pairs) {
    splits <- strsplit(pairs, " ") |> unlist()
    n <- length(splits)
    even <- seq(2, n, 2)
    # Since values come in value-color pairs
    result <- colors
    present <- splits[even]
    result[present] <- strtoi(splits[even - 1])
    result
}

parse_line <- function(line) {
    line <- sub("^Game \\d+:\\s+", "", line)
    draws <- strsplit(line, ";\\s+") |> unlist()
    pairs <- strsplit(draws, ",\\s+")
    lapply(pairs, parse_pairs) |>
        do.call(what = cbind)
}

validate <- function(game, combo) {
    min(combo - game) >= 0
}

power <- function(game) {
    asplit(game, MARGIN = 1) |>
        vapply(max, FUN.VALUE = numeric(1)) |>
        prod()
}

raw <- readLines("inputs/day2.txt")
processed <- lapply(raw, parse_line)

included <- c(red = 12, green = 13, blue = 14)
valid <- vapply(processed, validate, combo = included, FUN.VALUE = logical(1))
part1 <- sum(which(valid))
print(part1)

part2 <- vapply(processed, power, FUN.VALUE = numeric(1)) |>
    sum()
print(part2)
