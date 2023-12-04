parse_line <- function(line) {
    gsub("^Card\\s\\d+:\\s+", "", line) |>
        strsplit("\\s+\\|\\s+") |>
        unlist() |>
        lapply(\(x) strsplit(x, "\\s+")) |>
        lapply(unlist) |>
        lapply(strtoi)
}

matching <- function(pair) sum(pair[[2]] %in% pair[[1]])

points <- function(pair) {
    value <- matching(pair) - 1
    floor(2^value)
}

draw <- function(cards, won) {
    n <- length(cards)
    held <- rep(1, length.out = n)

    for (current in seq_len(n - 1)) {
        draws <- held[[current]]
        result <- won[[current]]
        if (result > 0) {
            received <- seq(current + 1, current + result, 1)
            # Clamp to number of cards
            received <- received[received <= n]
            held[received] <- held[received] + draws
        }
    }
    sum(held)
}

raw <- readLines("inputs/day4.txt")
processed <- lapply(raw, parse_line)
won <- vapply(processed, matching, FUN.VALUE = numeric(1))
part1 <- floor(2^(won - 1)) |>
    sum()
print(part1)

part2 <- draw(processed, won)
print(part2)
