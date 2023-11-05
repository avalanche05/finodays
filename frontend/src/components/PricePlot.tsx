import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { CfaPriceHistory } from '../api/models';

type Props = {
    cfaImageId: number;
    cfaTitle: string;
};

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top' as const,
        },
        title: {
            display: true,
            text: 'Цена актива',
        },
    },
};

const PricePlot = ({ cfaImageId, cfaTitle }: Props) => {
    const { rootStore } = useStores();
    const [priceHistory, setPriceHistory] = useState<CfaPriceHistory[] | null>(null);

    useEffect(() => {
        async function fetchCfaPricePrediction() {
            const fetchedPriceHistory = await rootStore.getCfaPriceHistory(cfaImageId);

            setPriceHistory(fetchedPriceHistory);
        }
        fetchCfaPricePrediction();
    }, [cfaImageId, rootStore]);

    const prepareData = (priceHistory: CfaPriceHistory[] | null) => {
        if (!priceHistory) {
            return {
                labels: [],
                datasets: [],
            };
        }

        const date = new Date();
        date.setDate(date.getDate() - 4);

        const labels = priceHistory.map(() => {
            date.setHours(date.getHours() + 1);
            return `${date.getDate()}.${date.getMonth() + 1} ${date.getHours()}:00`;
        });

        console.log(labels);

        const datasets = [
            {
                label: cfaTitle,
                data: priceHistory.map(({ price }) => price),
                borderColor: '#1677ff',
            },
        ];

        return {
            labels,
            datasets,
        };
    };

    return (
        <>
            <div style={{ width: '100%' }}>
                <Line
                    width='100%'
                    height='100px'
                    options={options}
                    data={prepareData(priceHistory)}
                />
            </div>
        </>
    );
};

export default PricePlot;
