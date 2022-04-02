def non_dominated_sorting(self, population: typing.Dict[int, BacktestResults]) -> typing.List[
    typing.List[BacktestResults]]:
    fronts = []

    for id_1, indiv_1 in population.items():
        for id_2, indiv_2 in population.items():
            if (indiv_1.pnl >= indiv_2.pnl) and (indiv_1.max_dd <= indiv_2.max_dd) and (
                    indiv_1.pct_win >= indiv_2.pct_win) and (
                    indiv_1.max_sl_row <= indiv_2.max_sl_row) and (indiv_1.max_tp_row >= indiv_2.max_tp_row) and (
                    indiv_1.total_trades >= indiv_2.total_trades) and (
                    (indiv_1.pnl > indiv_2.pnl) or (indiv_1.max_dd < indiv_2.max_dd) or (
                    indiv_1.pct_win > indiv_2.pct_win) or (indiv_1.max_sl_row < indiv_2.max_sl_row) or (
                            indiv_1.max_tp_row > indiv_2.max_tp_row) or (indiv_1.total_trades > indiv_2.total_trades)):

                indiv_1.dominates.append(id_2)

            elif (indiv_2.pnl >= indiv_1.pnl) and (indiv_2.max_dd <= indiv_1.max_dd) and (
                    indiv_2.pct_win >= indiv_1.pct_win) and (
                    indiv_2.max_sl_row <= indiv_1.max_sl_row) and (indiv_2.max_tp_row >= indiv_1.max_tp_row) and (
                    indiv_2.total_trades >= indiv_1.total_trades) and (
                    (indiv_2.pnl > indiv_1.pnl) or (indiv_2.max_dd < indiv_1.max_dd) or (
                    indiv_2.pct_win > indiv_1.pct_win) or (indiv_2.max_sl_row < indiv_1.max_sl_row) or (
                            indiv_2.max_tp_row > indiv_1.max_tp_row) or (indiv_2.total_trades > indiv_1.total_trades)):

                indiv_1.dominated_by += 1

        if indiv_1.dominated_by == 0:
            if len(fronts) == 0:
                fronts.append([])
            fronts[0].append(indiv_1)
            indiv_1.rank = 0

    i = 0

    while True:

        fronts.append([])

        for indiv_1 in fronts[i]:
            for indiv_2_id in indiv_1.dominates:
                population[indiv_2_id].dominated_by -= 1
                if population[indiv_2_id].dominated_by == 0:
                    fronts[i + 1].append(population[indiv_2_id])
                    population[indiv_2_id].rank = i + 1

        if len(fronts[i + 1]) > 0:
            i += 1
        else:
            del fronts[-1]
            break

    return fronts