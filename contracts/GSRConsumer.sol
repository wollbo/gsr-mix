pragma solidity ^0.6.7;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";


contract GSRConsumer {

    AggregatorV3Interface internal xau;
    AggregatorV3Interface internal xag;

    // Kovan XAU: 0xc8fb5684f2707C82f28595dEaC017Bfdf44EE9c5
    // Kovan XAG: 0x4594051c018Ac096222b5077C3351d523F93a963
    // returns round_id, answer, started_at, updated_at, answered_in

    constructor(address AggregatorAu, address AggregatorAg) public {
        xau = AggregatorV3Interface(AggregatorAu);
        xag = AggregatorV3Interface(AggregatorAg);
    }

    function get_latest_xau() public view returns (uint80, int, uint, uint, uint80) {
        return xau.latestRoundData();
    }

    function get_latest_xag() public view returns (uint80, int, uint, uint, uint80) {
        return xag.latestRoundData();
    }

    function get_historical_xau(uint80 round_id) public view returns (uint80, int, uint, uint, uint80) {
        return xau.getRoundData(round_id);
    }

    function get_historical_xag(uint80 round_id) public view returns (uint80, int, uint, uint, uint80) {
        return xag.getRoundData(round_id);
    }
} 