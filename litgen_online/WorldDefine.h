#ifndef _WORLD_DEFINE_H_
#define _WORLD_DEFINE_H_
#include <geometry.h>
#include <server.h>
#include "MedusaCore_export.h"
/************************************************************************/
/*                       ObjectPoseT                                    */
/************************************************************************/
class ObjectPoseT {
public:
    ObjectPoseT() : _valid(false), _pos(CGeoPoint(-9999, -9999)),_rawPos(CGeoPoint(-9999, -9999)) { }
    const CGeoPoint& Pos() const {
        return _pos;
    }
    const CGeoPoint& RawPos() const {
        return _rawPos;
    }
    double RawDir() const {
        return _rawDir;
    }
    void SetPos(double x, double y) {
        _pos = CGeoPoint(x, y);
    }
    void SetPos(const CGeoPoint& pos) {
        _pos = pos;
    }
    double X() const {
        return _pos.x();
    }
    double Y() const {
        return _pos.y();
    }
    void SetVel(double x, double y) {
        _vel = CVector(x, y);
    }
    void SetVel(const CVector& vel) {
        _vel = vel;
    }
    void SetRawVel(double x, double y) {
        _rawVel = CVector(x, y);
    }
    void SetRawVel(const CVector& vel) {
        _rawVel = vel;
    }
    void SetAcc(double x, double y) {
        _acc = CVector(x, y);
    }
    void SetAcc(const CVector& acc) {
        _acc = acc;
    }
    const CVector& Vel() const {
        return _vel;
    }
    const CVector& RawVel() const {
        return _rawVel;
    }

    void SetTargetVel(const CVector& target_vel) {
        _target_vel = target_vel;
    }
    const CVector& TargetVel() const {
        return _target_vel;
    }

    const CVector& Acc() const {
        return _acc;
    }
    double VelX() const {
        return _vel.x();
    }
    double VelY() const {
        return _vel.y();
    }
    double AccX() const {
        return _acc.x();
    }
    double AccY() const {
        return _acc.y();
    }
    void SetValid(bool v) {
        _valid = v;
    }
    bool Valid() const {
        return _valid;
    }
    void SetRawPos(double x, double y) {
        _rawPos = CGeoPoint(x, y);
    }
    void SetRawPos(const CGeoPoint& pos) {
        _rawPos = pos;
    }
    void SetRawDir(double rawdir) {
        _rawDir = rawdir;
    }
private:
    CGeoPoint _pos;
    CGeoPoint _rawPos; // 视觉的原始信息，没有经过卡尔曼滤波
    CVector _vel;
    CVector _rawVel;
    CVector _acc;
    bool _valid;
    double _rawDir;

    CVector _target_vel;
};
/************************************************************************/
/*                      VisionObjectT                                   */
/************************************************************************/
class VisionObjectT {
public:
    VisionObjectT() { }
    const CVector3 RealPos() const{
        return _realPos;
    }
    const CGeoPoint& ChipPredictPos() const {
        return _chipPredict;
    }
    // if get pos=CGeoPoint(10000,10000), then it hasn't been calculated already, gh
    const CGeoPoint& BestChipPredictPos() const{
        return _bestChipPredictPos;
    }
    const CGeoPoint& SecondChipPos() const{
        return _secondChipPos;
    }
    const CVector3& chipKickVel() const{
        return _chipKickVel;
    }
    double ChipFlyTime() const{
        return _chipFlyTime;
    }
    double ChipRestFlyTime() const{
        return _chipRestFlyTime;
    }
    // get chip state, gh
    bool ChipBallState() const{
        return _chipBallState;
    }
    void SetRealPos(const CVector3& realPos){
        _realPos = CVector3(realPos.x(), realPos.y(), realPos.z());
    }
    void SetRealPos(double x, double y ,double z) {
        _realPos = CVector3(x, y, z);
    }
    void SetChipPredict(const CGeoPoint& chipPos) {
        _chipPredict = chipPos;
    }
    void SetChipPredict(double x, double y) {
        _chipPredict =  CGeoPoint(x, y);
    }
    void SetBestChipPredictPos(double x, double y){
        _bestChipPredictPos = CGeoPoint(x, y);
    }
    void SetSecondChipPos(double x, double y){
        _secondChipPos = CGeoPoint(x, y);
    }
    void SetChipFlyTime(double t){
        _chipFlyTime = t;
    }
    void SetChipRestFlyTime(double t){
        _chipRestFlyTime = t;
    }
    void SetChipKickVel(double x, double y, double z) {
        _chipKickVel = CVector3(x, y, z);
    }
    void SetChipBallState(int state){
        _chipBallState = (state == ballState::_chip_pass);
    }
    void SetValidCount(int v) {
        _validCount=v;
    }
    int ValidCount()const {
        return _validCount;
    }
    int LastToucher()const {
        return _lastToucher;
    }
    void SetLastToucher(int id){
        _lastToucher = id;
    }


private:
    CGeoPoint _chipPredict; // 挑球预测 for every time
    CGeoPoint _bestChipPredictPos; // the best/stable chip predict pos, gh
    CGeoPoint _secondChipPos; // 第二落球點
    CVector3 _realPos;
    CVector3 _chipKickVel;
    double _chipFlyTime;
    double _chipRestFlyTime;
    bool _chipBallState; // is chip or not, gh

    int _validCount;
    int _lastToucher;
};
/************************************************************************/
/*                       BallVisionT                                  */
/************************************************************************/
class MEDUSACORE_API  BallVisionT : public ObjectPoseT, public VisionObjectT {

};
/************************************************************************/
/*                        机器人姿态数据结构                               */
/************************************************************************/
struct PlayerPoseT : public ObjectPoseT { // 目标信息
public:
    PlayerPoseT() : _dir(0), _rotVel(0) { }
    double Dir() const {
        return _dir;
    }
    void SetDir(double d) {
        _dir = d;
    }
    double RotVel() const {
        return _rotVel;
    }
    void SetRotVel(double d) {
        _rotVel = d;
    }
    double RawRotVel() const {
        return _rawRotVel;
    }
    void SetRawRotVel(double d) {
        _rawRotVel = d;
    }
    double ImuDir() const {
        return _imuDir;
    }
    double ImuRotateVel() const {
        return _imuRotateVel;
    }
    void SetImuDir(double imudir) {
        //modified 2020.9.17
        if (abs(imudir) < 1e-5) {
            _imuDir = _dir;
        }
        else{
            _imuDir = imudir;
        }
    }
    void SetImuRotateVel(double imurotatevel) {
        _imuRotateVel = imurotatevel;
    }
private:
    double _dir; // 朝向
    double _rotVel; // 旋转速度
    double _rawRotVel;
    double _imuDir;
    double _imuRotateVel;
};
/************************************************************************/
/*                      PlayerTypeT                                     */
/************************************************************************/
class PlayerTypeT {
public:
    PlayerTypeT(): _type(0) {}
    void SetType(int t) {
        _type = t;
    }
    int Type() const {
        return _type;
    }
private:
    int _type;
};
/************************************************************************/
/*                       PlayerVisionT                                  */
/************************************************************************/
class MEDUSACORE_API PlayerVisionT : public PlayerPoseT, public VisionObjectT, public PlayerTypeT {

};

/************************************************************************/
/*                        机器人能力数据结构                               */
/************************************************************************/
struct PlayerCapabilityT {
    PlayerCapabilityT(): maxAccel(0), maxSpeed(0), maxAngularAccel(0), maxAngularSpeed(0), maxDec(0), maxAngularDec(0) {}
    double maxAccel; // 最大加速度
    double maxSpeed; // 最大速度
    double maxAngularAccel; // 最大角加速度
    double maxAngularSpeed; // 最大角速度
    double maxDec;          // 最大减速度
    double maxAngularDec;   // 最大角减速度
    double maxSpeedX; // 最大纵向速度 by Tyh
	double maxSpeedY; // 最大横向速度 by Tyh
};
#endif // _WORLD_DEFINE_H_
