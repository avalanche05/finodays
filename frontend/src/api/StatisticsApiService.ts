import axios from 'axios';
import { IStatisctics, IUserStatistics } from './models';
import { API_URL } from '../config';

class StatisticsApiService {
    public async fetchStatistics(): Promise<IStatisctics> {
        const response = await axios.get<IStatisctics>(`${API_URL}/statistic`);

        return response.data;
    }

    public async fetchUsersStatistics(): Promise<IUserStatistics[]> {
        const response = await axios.get<IUserStatistics[]>(`${API_URL}/statistic/score`);

        return response.data;
    }
}

export const StatisticsApiServiceInstanse = new StatisticsApiService();
