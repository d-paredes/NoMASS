// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef CONTRACT_NODE_TREE_HPP_
#define CONTRACT_NODE_TREE_HPP_

#include <iostream>
#include <memory>

//**********************************************************************

/**
 * @brief Template class of the contract tree
 * @details Template class of the contract tree
 */
template <class T>
class Contract_Node_Tree
    {
    public:
        virtual bool compare(const T &insert) const = 0;
        virtual void makeLeft() = 0;
        virtual void makeRight() = 0;
        virtual bool isNodeRemoveable(
            const std::shared_ptr<Contract_Node_Tree<T>> & ptr) const = 0;
        virtual bool isRemoveable() const = 0;

        bool isLeftNull()
            {
            return pLeft == nullptr;
            }

        bool isRightNull()
            {
            return pRight == nullptr;
            }

        T findRightEdge()
            {
            T ret = nodeObject;
            if (pRight)
                {
                if (isNodeRemoveable(pRight))
                    {
                    pRight = nullptr;
                    }
                else
                    {
                    ret = pRight->findRightEdge();
                    }
                }
            if (isAssigned && isRemoveable())
                {
                isAssigned = false;
                nodeObject = NULL;
                }
            if (pLeft && isAssigned == false)
                {
                if (isNodeRemoveable(pLeft))
                    {
                    pLeft = nullptr;
                    }
                else
                    {
                    ret = pLeft->findRightEdge();
                    }
                }
            if (ret == nullptr && (pRight != nullptr || pLeft != nullptr))
                {
                ret = findRightEdge();
                }
            return ret;
            }

        T findLeftEdge()
            {
            if (pLeft)
                {
                if (isNodeRemoveable(pLeft))
                    {
                    pLeft  = nullptr;
                    }
                else
                    {
                    return pLeft->findLeftEdge();
                    }
                }
            if (isAssigned && isRemoveable())
                {
                isAssigned = false;
                nodeObject = NULL;
                }
            if (pRight && isAssigned == false)
                {
                if (isNodeRemoveable(pRight))
                    {
                    pRight  = nullptr;
                    }
                else
                    {
                    return pRight->findLeftEdge();
                    }
                }
            return nodeObject;
            }

        T popLeftEdge()
            {
            T ret;
            if (pLeft)
                {
                ret = pLeft->popLeftEdge();
                if(ret == nullptr)
                    {
                    pLeft = nullptr;
                    }
                }
            if (ret == nullptr && isAssigned)
                {
                isAssigned = false;
                ret = nodeObject;
                nodeObject = NULL;
                }
            if (pRight && ret == nullptr)
                {
                ret = pRight->popLeftEdge();
                if(ret == nullptr)
                    {
                    pRight = nullptr;
                    }
                }
            return ret;
            }

        void insert(const T & insert, double value)
            {
            if (nodeObject == NULL)
                {
                nodeObject = insert;
                this->value = value;
                isAssigned = true;
                }
            else
                {
                if (value < this->value)
                    {
                    if (!pLeft)
                        {
                        makeLeft();
                        }
                    pLeft->insert(insert, value);
                    }
                else
                    {
                    if (!pRight)
                        {
                        makeRight();
                        }
                    pRight->insert(insert, value);
                    }
                }
            }

        const T getNodeObject() const
            {
            return nodeObject;
            }

        void clear()
            {
            pLeft.reset();
            pRight.reset();
            isAssigned = false;
            nodeObject = NULL;
            }

    protected:
        T nodeObject;
        Contract_Node_Tree() {}
        std::shared_ptr<Contract_Node_Tree<T>> pLeft;
        std::shared_ptr<Contract_Node_Tree<T>> pRight;

    private:
        bool isAssigned = false;
        double value;
    };

//**********************************************************************

#endif  // CONTRACT_NODE_TREE_HPP_
