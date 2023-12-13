symmetric_col <- function(arr, col, find = FALSE) {
    # Fold line right
    extent <- min(col, ncol(arr) - col)
    left <- arr[, (col - extent + 1):col]
    right <- arr[, (col + extent):(col + 1)]
    if (find) {
        sum(left != right) == 1
    } else {
        all(left == right)
    }
}
symmetric_row <- function(arr, row, find = FALSE) {
    # Fold line down
    extent <- min(row, nrow(arr) - row)
    left <- arr[(row - extent + 1):row, ]
    right <- arr[(row + extent):(row + 1), ]
    if (find) {
        sum(left != right) == 1
    } else {
        all(left == right)
    }
}

solve <- function(mats) {
    part1 <- part2 <- 0

    for (mat in mats) {
        part1_done <- part2_done <- FALSE
        for (i in seq_len(ncol(mat) - 1)) {
            if (!part1_done && symmetric_col(mat, i)) {
                part1 <- part1 + i
                part1_done <- TRUE
            }
            if (!part2_done && symmetric_col(mat, i, TRUE)) {
                part2 <- part2 + i
                part2_done <- TRUE
            }
            if (part1_done && part2_done) break
        }
        part1_done <- part2_done <- FALSE
        for (i in seq_len(nrow(mat) - 1)) {
            if (!part1_done && symmetric_row(mat, i)) {
                part1 <- part1 + i * 100
                part1_done <- TRUE
            }
            if (!part2_done && symmetric_row(mat, i, TRUE)) {
                part2 <- part2 + i * 100
                part2_done <- TRUE
            }
            if (part1_done && part2_done) break
        }
    }
    c(part1, part2)
}
parse_mat <- function(lines) {
    result <- do.call(strsplit(lines, ""), what = rbind)
    result == "#"
}

raw <- readChar("inputs/day13.txt", file.info("inputs/day13.txt")$size)
parts <- strsplit(raw, "\n\n") |>
    unlist() |>
    strsplit("\n") |>
    lapply(parse_mat)
parts <- solve(parts)
print(parts[[1]])
print(parts[[2]])
