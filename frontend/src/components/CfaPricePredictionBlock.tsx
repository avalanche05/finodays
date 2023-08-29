import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from 'recharts';

type Props = {
    cfaImageId: number;
};

const CfaPricePredictionBlock = ({ cfaImageId }: Props) => {
    const { rootStore } = useStores();
    const [cfaPricePrediction, setCfaPricePrediction] = useState<number[] | null>(null);

    useEffect(() => {
        async function fetchCfaPricePrediction() {
            const predictions = await rootStore.getCfaPricePrediction(cfaImageId);

            setCfaPricePrediction(predictions);
        }
        fetchCfaPricePrediction();
    }, [cfaImageId, rootStore]);

    const prepareData = (predictions: number[] | null) => {
        if (!predictions) {
            return [];
        }

        const date = new Date();

        return predictions.map((prediction) => ({
            name: new Date(date.setDate(date.getDate() + 1)).getDate(),
            pv: prediction,
        }));
    };

    return (
        <div style={{ width: '100%', height: 200, marginTop: 20 }}>
            <ResponsiveContainer width='100%' height='100%'>
                <LineChart
                    width={500}
                    height={300}
                    data={prepareData(cfaPricePrediction)}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray='3 3' />
                    <XAxis dataKey='name' />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type='monotone' dataKey='pv' stroke='#8884d8' activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default CfaPricePredictionBlock;
