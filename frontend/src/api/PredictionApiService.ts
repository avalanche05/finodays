import axios from 'axios';
import { API_URL } from '../config';
import authHeader from '../utils/authHeader';
import { CfaPricePrediction } from './models/CfaPricePrediction';

class PredictionApiService {
    public async fetchCfaPricePrediction(cfaImageId: number): Promise<number[]> {
        const response = await axios.get<CfaPricePrediction>(
            `${API_URL}/cfa-image/pred-price/${cfaImageId}`,
            {
                headers: authHeader(),
            }
        );

        return response.data.predictions;
    }
}

export const PredictionApiServiceInstanse = new PredictionApiService();
