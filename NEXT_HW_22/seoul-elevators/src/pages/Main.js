import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './Main.css';

// Fix for default icon issue with Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const Main = () => {
    const [data, setData] = useState([]);
    const [districts, setDistricts] = useState([]);
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [stations, setStations] = useState([]);
    const [selectedStation, setSelectedStation] = useState(null);
    const [elevatorLocations, setElevatorLocations] = useState([]);

    useEffect(() => {
        axios.get('/data.json').then((response) => {
            setData(response.data);
            const uniqueDistricts = Array.from(new Set(response.data.map((item) => item.SGG_NM)));
            setDistricts(uniqueDistricts.map((district) => ({ value: district, label: district })));
        });
    }, []);

    const handleDistrictChange = (selectedOption) => {
        setSelectedDistrict(selectedOption);
        const stationsInDistrict = data
            .filter((item) => item.SGG_NM === selectedOption.value && item.SW_NM)
            .reduce((acc, item) => {
                if (!acc.find((station) => station.SW_NM === item.SW_NM)) {
                    acc.push(item);
                }
                return acc;
            }, []);
        setStations(stationsInDistrict);
    };

    const handleStationClick = (station) => {
        const elevators = data.filter((item) => item.SW_NM === station.SW_NM);
        setSelectedStation(station);
        setElevatorLocations(elevators);
    };

    return (
        <div className="app-container">
            <h1 className="app-title">서울 지하철역 엘레베이터 위치 찾기</h1>
            <Select
                className="district-select"
                options={districts}
                onChange={handleDistrictChange}
                placeholder="구를 선택하세요!"
            />
            {stations.length > 0 && (
                <div className="stations-container">
                    <h2 className="stations-title">Stations in {selectedDistrict.label}</h2>
                    <ul className="stations-list">
                        {stations.map((station) => (
                            <li
                                key={station.NODE_ID}
                                onClick={() => handleStationClick(station)}
                                className="station-item"
                            >
                                {station.SW_NM}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            {selectedStation && (
                <MapContainer
                    center={[37.5665, 126.978]}
                    zoom={15}
                    style={{ height: '600px', width: '100%' }}
                    className="map-container"
                >
                    <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                    {elevatorLocations.map((elevator) => (
                        <Marker
                            key={elevator.NODE_ID}
                            position={[
                                parseFloat(elevator.NODE_WKT.split(' ')[1]),
                                parseFloat(elevator.NODE_WKT.split(' ')[0].replace('POINT(', '')),
                            ]}
                        >
                            <Popup>Elevator Location for {elevator.SW_NM}</Popup>
                        </Marker>
                    ))}
                    <ChangeView
                        center={[
                            parseFloat(elevatorLocations[0].NODE_WKT.split(' ')[1]),
                            parseFloat(elevatorLocations[0].NODE_WKT.split(' ')[0].replace('POINT(', '')),
                        ]}
                        zoom={17}
                    />
                </MapContainer>
            )}
        </div>
    );
};

const ChangeView = ({ center, zoom }) => {
    const map = useMap();
    map.setView(center, zoom);
    return null;
};

export default Main;
