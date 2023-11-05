import { User } from '../../models/User';

export interface IStatisctics {
    transactions_count: number;
    transactions_count_increment: number;
    deals_count: number;
    deals_count_increment: number;
    turn: number;
    turn_increment: number;
    created_cfa_count: number;
    created_cfa_count_increment: number;
}

export interface IUserStatistics extends User {
    buy_count: number;
    buy_value: number;
    sell_count: number;
    sell_value: number;
}
