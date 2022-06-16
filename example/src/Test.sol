// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.4;

contract Test {
    uint256 public a;
    string public b;
    address public owner;

    constructor(uint256 _a, string memory _b) {
        a = _a;
        b = _b;
        owner = msg.sender;
    }

    function transferOwnership(address _owner, string memory _b) public {
        require(msg.sender == owner, "NOT_AUTHORIZED");
        owner = _owner;
        b = _b;
    }
}
