n_t <- 20
n_s <- 3
n_c <- 1000
v_state_names <- c("Up", "Down")
m_P <- matrix(c(0.50115473441, 0.49884526558, 0.53201970443, 0.46798029556), nrow = 2, ncol = 2, byrow = TRUE, dimnames = list(from = v_state_names, to = v_state_names))
print(m_P)
state_membership <- array(NA_real_, dim = c(n_t, n_s), dimnames = list(cycle = 1:n_t, state = v_state_names))
n_c = 252
state_membership[1, ] <- c(n_c, 0)
for (i in 2:n_t) {state_membership[i, ] <- state_membership[i - 1, ] %*% m_P }
print(state_membership)
